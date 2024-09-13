from fasthtml.common import *
from typing import List

# Define TR and TH and TD in case they're not imported
def TR(*content):
    return Tr(*content)

def TH(content, sort_by=None, current_sort=None):
    sort_icon = ""
    if sort_by == current_sort:
        sort_icon = " ▲"
    elif f"-{sort_by}" == current_sort:
        sort_icon = " ▼"
    return Th(A(content + sort_icon, href=f"?sort={sort_by}"))

def TD(content):
    return Td(content)

app = FastHTML()
rt = app.route

# Mock data representing Kubernetes pods
mock_pods = [
    {"name": "pod-1", "namespace": "default", "status": "Running"},
    {"name": "pod-2", "namespace": "kube-system", "status": "Pending"},
    {"name": "pod-3", "namespace": "dev", "status": "Running"},
]

def sort_pods(pods, sort_key):
    reverse = False
    if sort_key.startswith("-"):
        reverse = True
        sort_key = sort_key[1:]
    return sorted(pods, key=lambda x: x[sort_key], reverse=reverse)

def filter_pods(pods, status_filter):
    if status_filter:
        return [pod for pod in pods if pod['status'] == status_filter]
    return pods

# Create a table component to display pods
def PodTable(pods: List[dict], current_sort=None, status_filter=None) -> Div:
    pods = filter_pods(pods, status_filter)
    if current_sort:
        pods = sort_pods(pods, current_sort)
    
    headers = [("Name", "name"), ("Namespace", "namespace"), ("Status", "status")]
    header_row = [TH(header[0], sort_by=header[1], current_sort=current_sort) for header in headers]

    body_rows = [
        TR(
            TD(pod['name']),
            TD(pod['namespace']),
            TD(pod['status'])
        ) for pod in pods
    ]

    return Div(
        Table(
            Thead(TR(*header_row)),
            Tbody(*body_rows),
            style={'border-collapse': 'collapse'}
        ),
        style={
            'width': '100%',
            'border': '1px solid black',
            'text-align': 'left',
            'padding': '8px'
        }
    )

@rt('/')
def get(sort: str = None, status: str = None):
    return Div(
        H1('Kubernetes Pods Overview'),
        Form(
            Div(
                Label("Filter by status:"),
                Select(
                    Option("All", value="", selected=status is None),
                    Option("Running", value="Running", selected=status == "Running"),
                    Option("Pending", value="Pending", selected=status == "Pending"),
                    name="status"
                ),
                Button("Apply Filter", type="submit")
            ),
            method="get"
        ),
        PodTable(mock_pods, current_sort=sort, status_filter=status)
    )

serve()