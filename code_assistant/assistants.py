import os
from typing import List

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
from openai import OpenAI, BaseModel
from pydantic import Field

from code_assistant.util.constants.small_fasthtml_context import small_fasthtml_context
from code_assistant.util.file_util import get_mount_from_file


class TrueOrFalsePayload(BaseModel):
    answer: bool = Field(..., description="true or false")

    def to_string(self):
        return "True" if self.answer else "False"


class TrueOrFalseTool(ToolInterface):
    def call(self, result: TrueOrFalsePayload):
        return {"output": result}


class ManagerFactory:
    class ObservableList(ProgramCache):
        def __init__(self, app, *args):
            self.app = app
            super().__init__(*args)

        def append(self, item: StructuredProgramEntry) -> None:
            original_program_str = item.program.to_string(with_line_numbers=False)
            super().append(item)
            self.write_file_to_disk(item, original_program_str != item.program.to_string(with_line_numbers=False))

        def extend(self, iterable: List[StructuredProgramEntry]) -> None:
            original_program_strs = []
            for item in iterable:
                original_program_strs.append(item.program.to_string(with_line_numbers=False))

            super().extend(iterable)
            i = 0
            for item in iterable:
                self.write_file_to_disk(item, original_program_strs[i] != item.program.to_string(with_line_numbers=False))
                i += 1

        def insert(self, index: int, item: StructuredProgramEntry) -> None:
            original_program_str = item.program.to_string(with_line_numbers=False)
            super().insert(index, item)
            self.write_file_to_disk(item, original_program_str != item.program.to_string(with_line_numbers=False))

        def write_file_to_disk(self, item: StructuredProgramEntry, changed: bool) -> None:
            # if item.program.filename is not None and item.program_id != item.program.filename:
            if item.program.filename is not None:
                if changed or item.program_id != item.program.filename:
                    with open(f"generated_apps/{item.program.filename}", "w") as f:
                        f.write(item.program.to_string(with_line_numbers=False))
                    route = None
                    for app_route in self.app.routes:
                        path = f"/{item.program.filename.split('.')[0]}"
                        if app_route.path == path:
                            route = app_route
                            break
                    if route is not None:
                        self.app.routes.remove(route)
                    self.app.routes.append(get_mount_from_file(item.program.filename, item.program_id))

    def __init__(self, app):
        self.app = app
        self.client = patch(OpenAI())
        self.additional_instructions = [small_fasthtml_context]
        self.programs: List[StructuredProgramEntry] = self.ObservableList(self.app)
        self.setup_programs()
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
            model="openai/gpt-4o-2024-08-06",
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

    def setup_programs(self):
        for root, dirs, files in os.walk('generated_apps'):
            for file in files:
                if not file.endswith('.pyc'):
                    text = open(root + "/" + file).read()
                    try:
                        self.programs.append(
                            StructuredProgramEntry(
                                program_id=file,
                                program=StructuredProgram(
                                    lines=text.split("\n"),
                                    filename=file,
                                    language=file.split(".")[1]
                                )
                            )
                        )
                    except Exception as e:
                        print(e)
                        print(f"Failed to load {file} to program cache")
                        raise e
        print("setup complete")
