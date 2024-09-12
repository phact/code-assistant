import os
from typing import List, Dict

from astra_assistants import patch
from astra_assistants.astra_assistants_manager import AssistantManager
#from astra_assistants.tools.structured_code.delete import StructuredCodeDelete
#from astra_assistants.tools.structured_code.indent import StructuredCodeIndentRight, StructuredCodeIndentLeft
#from astra_assistants.tools.structured_code.insert import StructuredCodeInsert
from astra_assistants.tools.structured_code.program_cache import ProgramCache, StructuredProgramEntry, StructuredProgram
#from astra_assistants.tools.structured_code.replace import StructuredCodeReplace
from astra_assistants.tools.structured_code.rewrite import StructuredCodeRewrite
from astra_assistants.tools.structured_code.write import StructuredCodeFileGenerator
from astra_assistants.tools.tool_interface import ToolInterface
from code_assistant.constants.config import GENERATED_APPS_DIR
from openai import OpenAI
from pydantic import Field, BaseModel, field_validator

from code_assistant.constants.context.small_fasthtml_context import small_fasthtml_context
from code_assistant.util.file_util import get_mount_from_project


class TrueOrFalsePayload(BaseModel):
    answer: bool = Field(..., description="true or false")

    def to_string(self):
        return "True" if self.answer else "False"


class TrueOrFalseTool(ToolInterface):
    def call(self, result: TrueOrFalsePayload):
        return {"output": result}


class Project:
    def __init__(self, program_relations: List[Dict[str, str]] = []):
        # Make sure filename_to_program_id and program_id_to_filename are instance-level variables
        self.filename_to_program_id: Dict[str, str] = {}
        self.program_id_to_filename: Dict[str, str] = {}

        # If relations are passed in the constructor, add them
        for relation in program_relations:
            self.add_relation(relation["filename"], relation["program_id"])

    def add_relation(self, filename: str, program_id: str):
        """
        Method to add a new relation (filename, program_id) to the project.
        This will also update the reverse mapping (program_id_to_filename).
        """
        self.filename_to_program_id[filename] = program_id
        self.program_id_to_filename[program_id] = filename

    def get_filename_by_program_id(self, program_id: str) -> str:
        """Return the filename for the given program_id."""
        return self.program_id_to_filename.get(program_id)

    def get_program_id_by_filename(self, filename: str) -> str:
        """Return the program_id for the given filename."""
        return self.filename_to_program_id.get(filename)

# Define a Projects class to hold multiple projects
class Projects:
    def __init__(self):
        # This will store the list of projects
        self.projects: List[Project] = []

    def add_project(self, project: Project):
        """Method to add a new project to the Projects collection."""
        self.projects.append(project)

    def get_project(self, index: int) -> Project:
        """Return the project at the specified index."""
        return self.projects[index]

    def find_project_by_filename(self, filename: str) -> Project:
        """Find the project that contains a specific filename."""
        for project in self.projects:
            if filename in project.filename_to_program_id:
                return project
        return None

    def find_project_by_program_id(self, program_id: str) -> Project:
        """Find the project that contains a specific program_id."""
        for project in self.projects:
            if program_id in project.program_id_to_filename:
                return project
        return None

    def get_program_id_by_filename(self, filename: str) -> str:
        project = self.find_project_by_filename(filename)
        if project:
            return project.get_program_id_by_filename(filename)
        return None

    def get_filename_by_program_id(self, program_id: str) -> str:
        project = self.find_project_by_program_id(program_id)
        if project:
            return project.get_filename_by_program_id(program_id)
        return None


class ManagerFactory:
    class ObservableList(ProgramCache):
        def __init__(self, app, projects, *args):
            self.app = app
            self.projects = projects
            super().__init__(*args)

        def add(self, item: StructuredProgramEntry) -> None:
            original_program_id = self.latest_program_id_by_filename(item.program.filename)
            original_program_str = None
            if original_program_id is not None:
                original_program_str = self.cache.get(self.latest_program_id_by_filename(item.program.filename)).program.to_string(with_line_numbers=False)
            super().add(item)
            if original_program_str is not None or item.program.filename != item.program_id:
                self._write_if_changed(item, original_program_str)

        def extend(self, iterable: List[StructuredProgramEntry]) -> None:
            original_program_strs = []
            for item in iterable:
                original_program_str = self.cache.get(self.latest_program_id_by_filename(item.program.filename)).program.to_string(with_line_numbers=False)
                original_program_strs.append(original_program_str)
            super().extend(iterable)  # Use ProgramCache's extend method for dictionary-based storage

            for item in iterable:
                original_program_str = original_program_strs[item.program.id]
                self._write_if_changed(item, original_program_str)

        def _write_if_changed(self, item: StructuredProgramEntry, original_program_str: str) -> None:
            """
            Writes the program to disk if it has changed, and updates the app routes.
            """
            updated_program_str = item.program.to_string(with_line_numbers=False)
            if original_program_str != updated_program_str:
                self.write_file_to_disk(item)

        def write_file_to_disk(self, item: StructuredProgramEntry) -> None:
            """
            Writes the program file to disk and updates the app's routes.
            """
            if item.program.filename is not None:
                # Write the program to disk
                filepath = f"generated_apps/{item.program.filename}"
                if not os.path.exists(os.path.dirname(filepath)):
                    os.makedirs(os.path.dirname(filepath))
                with open(filepath, "w") as f:
                    f.write(item.program.to_string(with_line_numbers=False))

                # Update app routes
                self.update_app_routes(item)
                project = Project()
                project.add_relation(filename=item.program.filename, program_id=item.program_id)
                self.projects.add_project(project)

        def update_app_routes(self, item: StructuredProgramEntry) -> None:
            """
            Updates the app routes based on the program filename and ID.
            """
            filename_base = item.program.filename.replace('/app.py','')
            path = f"/{filename_base}"

            # Find the existing route if it exists and remove it
            existing_route = next((route for route in self.app.routes if route.path == path), None)
            if existing_route:
                self.app.routes.remove(existing_route)

            # Add a new route for the updated program
            self.app.routes.append(get_mount_from_project(filename_base, item.program_id))

        def latest_program_id_by_filename(self, filename: str) -> str:
            programEntry: StructuredProgramEntry | None = None
            for program_id in self.order:
                entry = self.cache[program_id]
                if entry.program.filename == filename:
                    programEntry = entry
            if hasattr(programEntry, "program_id"):
                return programEntry.program_id
            return programEntry

    def __init__(self, app):
        self.app = app
        self.client = patch(OpenAI())
        self.additional_instructions = [small_fasthtml_context]
        self.projects: Projects = Projects()
        self.programs: ProgramCache = self.ObservableList(self.app, self.projects)
        self.setup_projects_and_programs()
        self.code_generator = StructuredCodeFileGenerator(self.programs)
        self.code_rewriter = StructuredCodeRewrite(self.programs)
        #self.code_replace = StructuredCodeReplace(self.programs)
        #self.code_insert = StructuredCodeInsert(self.programs)
        #self.code_delete = StructuredCodeDelete(self.programs)
        #self.code_indent_right = StructuredCodeIndentRight(self.programs)
        #self.code_indent_left = StructuredCodeIndentLeft(self.programs)
        #self.true_or_false_tool = TrueOrFalseTool()

        self.tools = [self.code_generator, self.code_rewriter]

        self.code_manager = AssistantManager(
            instructions="Use the structured code tools to generate code to help the user. If you still need to make more changes based on an edit, say so.",
            tools=self.tools,
            #model="openai/chatgpt-4o-latest",
            model=app.state.model,
            #model="openai/gpt-4o-mini",
            #assistant_id="asst_6FH38BvdFdtzUBu7UK0U0H3Be2sgkJ7O",
            #thread_id="thread_94kTIBLZI918vFI6OLzpnOFqmiH9SI7L"
        )

    def set_program_ids(self, program_id):
        self.code_rewriter.set_program_id(program_id)
        #self.code_replace.set_program_id(program_id)
        #self.code_insert.set_program_id(program_id)
        #self.code_delete.set_program_id(program_id)
        #self.code_indent_left.set_program_id(program_id)
        #self.code_indent_right.set_program_id(program_id)

    def setup_projects_and_programs(self):
        for root, dirs, files in os.walk(GENERATED_APPS_DIR):
            project_name = os.path.basename(root)
            for file in files:
                if not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        text = f.read()
                    try:
                        # When reading from disk on init the filename equals the project name. This stops being the case once we edit.
                        project = Project()
                        project.add_relation(filename=f'{project_name}/app.py', program_id=project_name)
                        self.projects.add_project(project)

                        program = StructuredProgramEntry(
                            program_id=project_name,
                            program=StructuredProgram(
                                lines=text.split("\n"),
                                filename=f"{project_name}/app.py",
                                language=file.split(".")[-1]
                            )
                        )
                        self.programs.add(
                            program
                        )
                    except Exception as e:
                        print(e)
                        print(f"Failed to load {file} to program cache")
                        raise e
        print("setup complete")
