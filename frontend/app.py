
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F8F5FF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F3E8FF;
}

/* Buttons */
.stButton > button {
    background-color: #F9A8D4;
    color: #4C1D95;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #F472B6;
    color: white;
}

/* Text Inputs */
.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: #FFFFFF;
    border: 1px solid #E9D5FF;
    border-radius: 8px;
}

/* Select Boxes */
div[data-baseweb="select"] > div {
    background-color: white;
    border: 1px solid #E9D5FF;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #FBCFE8;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* Success Messages */
.stSuccess {
    border-radius: 10px;
}

/* Warning Messages */
.stWarning {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
API_BASE_URL = "http://127.0.0.1:8000"
# API HELPER
# ==========================
def api_call(method, endpoint, data=None, token=None):

    headers = {}

    params = {}

    if token:
        params["token"] = token

    try:

        if method == "GET":
            response = requests.get(
                f"{API_BASE_URL}{endpoint}",
                params=params
            )

        elif method == "POST":
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                params=params
            )

        elif method == "PATCH":
            response = requests.patch(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                params=params
            )
        elif method == "PUT":
            response = requests.put(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                params=params
            )

        elif method == "DELETE":
            response = requests.delete(
                f"{API_BASE_URL}{endpoint}",
                params=params
            )

        else:
            return None

        return response

    except requests.exceptions.ConnectionError:
        st.error("Backend server is not running.")
        return None


# ==========================
# SESSION STATE
# ==========================
if "logout_message" not in st.session_state:
    st.session_state.logout_message = False
if "success_message" not in st.session_state:
    st.session_state.success_message = None
if "page" not in st.session_state:
    st.session_state.page = "login"

if "token" not in st.session_state:
    st.session_state.token = None

if "email" not in st.session_state:
    st.session_state.email = None
    
if "selected_task_id" not in st.session_state:
    st.session_state.selected_task_id = None
       
if "edit_task" not in st.session_state:
    st.session_state.edit_task = None
    

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

if "confirm_logout" not in st.session_state:
    st.session_state.confirm_logout = False    

# ==========================
# REGISTER PAGE
# ==========================
def register_page():

    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if not email or not password:
            st.error("All fields are required")
            return
        if "@" not in email or "." not in email:
                        st.error("Enter a valid email address (example: user@gmail.com) ")
                        return

        if len(password) < 6:
                        st.error("Password must contain at least 6 characters")
                        return

        response = api_call(
            "POST",
            "/auth/register",
            {
                "email": email,
                "password": password
            }
        )

        if response is None:
            return

        if response.status_code == 200:
            st.session_state.logout_message = False
            st.session_state.success_message = "🎉 Welcome aboard! Your account has been created successfully."
            st.session_state.page = "login"
            st.rerun()

        else:
            st.error(response.json()["detail"])

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()


# ==========================
# LOGIN PAGE
# ==========================
def login_page():
    

    if st.session_state.get("logout_message", False):
        st.success("Logged out successfully")
        st.session_state.logout_message = False

    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None   

    st.title("Login")
    
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not email or not password:
            st.error("All fields are required")
            return

        response = api_call(
            "POST",
            "/auth/login",
            {
                "email": email,
                "password": password
            }
        )

        if response is None:
            return

        if response.status_code == 200:

            data = response.json()

            st.session_state.token = data["token"]
            st.session_state.email = email
            st.session_state.success_message = "✅ Login successful! Let's make today productive."

            st.session_state.page = "dashboard"

            st.rerun()

        else:
            st.error("Invalid credentials")

    st.subheader("New User?")

    if st.button("Register Here"):
        st.session_state.page = "register"
        st.rerun()


# ==========================
# ADD TASK PAGE
# ==========================
def add_task_page():

    st.title("Add Task")

    with st.form("task_form"):

        title = st.text_input("Title")

        description = st.text_area(
            "Description"
        )

        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"]
        )
        status = st.selectbox(
                                    "Status",
                                    ["pending", "in-progress", "done"]
                                )

        due_date = st.date_input(
            "Due Date"
        )

        submit = st.form_submit_button(
            "Create Task"
        )

        if submit:

            if not title:
                st.error("Title is required")
                return

            response = api_call(
                "POST",
                "/tasks/",
                {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "due_date": str(due_date)
                },
                st.session_state.token
            )

            if response.status_code == 201:
                        st.session_state.success_message = "Task created successfully"
                        st.session_state.page = "dashboard"
                        st.rerun()
            else:
                st.error(response.text)

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()
# ==========================
# VIEW TASK PAGE
# ==========================
def view_task_page():

    st.title("Task Details")

    task_id = st.session_state.selected_task_id

    response = api_call(
        "GET",
        f"/tasks/{task_id}",
        token=st.session_state.token
    )

    if response.status_code == 404:
        st.error("Task not found")
        st.session_state.page = "dashboard"
        st.rerun()

    if response.status_code == 403:
        st.error("Access denied")
        st.session_state.page = "dashboard"
        st.rerun()

    task = response.json()

    st.write("### Title")
    st.write(task["title"])

    st.write("### Description")
    st.write(task["description"])

    st.write("### Priority")
    st.write(task["priority"])

    st.write("### Status")

    if task["status"] == "done":
            st.success("Done")

    elif task["status"] == "in-progress":
            st.warning("In Progress")

    else:
            st.info("Pending")
            
    st.write("### Due Date")
    st.write(task["due_date"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Edit"):
                st.session_state.selected_task_id = task["id"]
                st.session_state.page = "edit_task"
                st.rerun()

    with col2:

                if st.button(
                                "Delete",
                                key="view_delete"
                            ):
                         st.session_state.confirm_delete = True

                if st.session_state.get("confirm_delete", False):

                                            st.warning(
                                            "Are you sure you want to delete this task?"
                                                        )

                                            c1, c2 = st.columns(2)

                                            with c1:
                                                if st.button(
                                                            "Yes, Delete",
                                                            key="confirm_yes"
                                                            ):

                                                    response = api_call(
                                                                            "DELETE",
                                                                            f"/tasks/{task_id}",
                                                                            token=st.session_state.token
                                                                        )

                                                    if response.status_code == 200:

                                                                    st.session_state.success_message = "Task deleted successfully"

                                                                    st.session_state.confirm_delete = False
                                                                    st.session_state.page = "dashboard"

                                                                    st.rerun()

                                            with c2:
                                                    if st.button(
                                                                    "Cancel",
                                                                    key="confirm_no"
                                                                ):

                                                        st.session_state.confirm_delete = False
                                                        st.rerun()

    with col3:
        if st.button("Back"):
            st.session_state.page = "dashboard"
            st.rerun()


# ==========================
# DASHBOARD
# ==========================
def dashboard_page():

    st.title("Task Dashboard")
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None

    st.sidebar.write(
        f"Logged in as: {st.session_state.email}"
    )

    if st.sidebar.button("Add Task"):
        st.session_state.page = "add_task"
        st.rerun()

    if st.sidebar.button("Logout"):
                    st.session_state.confirm_logout = True

    if st.session_state.get("confirm_logout", False):

                st.sidebar.warning(
                                    "Are you sure you want to logout?"
                                    )

                if st.sidebar.button("Yes, Logout"):

                    st.session_state.token = None
                    st.session_state.email = None
                    st.session_state.selected_task_id = None
                    st.session_state.confirm_logout = False

                    st.session_state.logout_message = True
                    st.session_state.page = "login"

                    st.rerun()

                if st.sidebar.button(
                                        "Cancel Logout"
                                    ):
                        st.session_state.confirm_logout = False
                        st.rerun()

    token = st.session_state.token

    summary_response = api_call(
        "GET",
        "/tasks/summary",
        token=token
    )

    if summary_response and summary_response.status_code == 200:

        summary = summary_response.json()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
                    "Total",
                    summary["total"]
                )

        c2.metric(
                    "Pending",
                    summary["pending"]
                )

        c3.metric(
                    "In Progress",
                    summary["in_progress"]
                )

        c4.metric(
                    "Done",
                    summary["done"]
                )
    st.divider()

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        status_filter = st.selectbox(
        "Status",
        ["All", "pending", "in-progress", "done"]
    )

    with col_filter2:
        priority_filter = st.selectbox(
        "Priority",
        ["All", "low", "medium", "high"]
    )

    tasks_response = api_call(
        "GET",
        "/tasks/",
        token=token
    )

    if tasks_response and tasks_response.status_code == 200:

        tasks = tasks_response.json()
        task_names = [task["title"] for task in tasks]

        selected_task = st.selectbox(
                                    "Select Task",
                                    ["All Tasks"] + task_names
                                    )
        if selected_task != "All Tasks":
                                    tasks = [
                                                task for task in tasks
                                                    if task["title"] == selected_task
                                            ]
        if status_filter != "All":
            tasks = [
                        t for t in tasks
                        if t["status"] == status_filter
                    ]

        if priority_filter != "All":
            tasks = [
                        t for t in tasks
                        if t["priority"] == priority_filter
                    ]



        if tasks:

            df = pd.DataFrame(tasks)

            if "owner_email" in df.columns:
                df = df.drop(
                    columns=["owner_email"]
                )

            st.dataframe(
                            df,
                            width="stretch"
                        )

            st.subheader("Task Actions")

            for task in tasks:

                col1, col2, col3, col4, col5 = st.columns([4,1,1,1,1]
                )
                

                col1.write(
                            f"{task['title']} ({task['status']})"
                            )

             # VIEW
                if col2.button(
                                "View Task",
                                key=f"view_{task['id']}"
                                ):
                    st.session_state.selected_task_id = task["id"]
                    st.session_state.page = "view_task"
                    st.rerun()

    # UPDATE
                if col3.button(
                                    "Edit Task",
                                    key=f"update_{task['id']}"
                                ):
                                        st.session_state.selected_task_id = task["id"]
                                        st.session_state.page = "edit_task"
                                        st.rerun()

    # DONE
                if (
                        task["status"] != "done"
                        and col4.button(
                            "Done",
                            key=f"done_{task['id']}"
                         )
                    ):

                    response = api_call(
                                            "PATCH",
                                            f"/tasks/{task['id']}/status",
                                            {"status": "done"},
                                            token
                                        )

                    if response.status_code == 200:
                     st.session_state.success_message = "Task marked as done"
                     st.rerun()
                    else:
                        st.error(response.text)

    # DELETE
                if col5.button(
                                "Delete",
                                key=f"delete_{task['id']}"
                                ):
                    st.session_state.delete_task_id = task["id"]

                if (
                                "delete_task_id" in st.session_state
                                and st.session_state.delete_task_id == task["id"]
                    ):

                    st.warning(
                    f"Are you sure you want to delete '{task['title']}'?"
                                )

                    c1, c2 = st.columns(2)

                    with c1:
                            if st.button(
                                         "Yes",
                                        key=f"yes_{task['id']}"
                                        ):

                                    response = api_call(
                                                        "DELETE",
                                                        f"/tasks/{task['id']}",
                                                        token=token
                                                        )

                                    if response.status_code == 200:
                                        st.session_state.success_message = "Task deleted successfully"
                                        del st.session_state.delete_task_id
                                        st.rerun()

                    with c2:
                            if st.button(
                                                "No",
                                                key=f"no_{task['id']}"
                                        ):
                                    del st.session_state.delete_task_id
                                    st.rerun()
                    
                    

        else:
            st.info("No tasks found")
# -=====================
#   Edit_page
#=======================            
def edit_task_page():

    task_id = st.session_state.selected_task_id

    response = api_call(
        "GET",
        f"/tasks/{task_id}",
        token=st.session_state.token
    )

    if response.status_code != 200:
        st.error("Task not found")
        st.session_state.page = "dashboard"
        st.rerun()

    task = response.json()

    st.title("Update Task")

    title = st.text_input(
        "Title",
        value=task["title"]
    )

    description = st.text_area(
        "Description",
        value=task["description"]
    )

    priority_list = ["low", "medium", "high"]

    priority = st.selectbox(
                            "Priority",
                             priority_list,
                             index=priority_list.index(task["priority"])
                            )
    status_list = [
                        "pending",
                        "in-progress",
                        "done"
                    ]

    status = st.selectbox(
                            "Status",
                            status_list,
                            index=status_list.index(task["status"])
                        )
    

    

    due_date = st.date_input(
                                "Due Date",
                                value=datetime.strptime(
                                                            task["due_date"],
                                                                "%Y-%m-%d"
                                                        ).date()
                            )

    if st.button("Update Task"):
        if not title.strip():
            st.error("Title is required")
            return
        response = api_call(
            "PUT",
            f"/tasks/{task['id']}",
            {
                "title": title,
                "description": description,
                "priority": priority,
                "status": status,
                "due_date":str( due_date)
            },
            st.session_state.token
        )

        if response.status_code == 200:

            st.session_state.success_message = "Task updated successfully"

            st.session_state.page = "dashboard"

            st.rerun()

        else:
            st.error(response.text)

    if st.button("Cancel"):

        st.session_state.page = "dashboard"

        st.rerun() 


# ==========================
# PAGE ROUTING
# ==========================
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "register":
    register_page()

elif st.session_state.page == "dashboard":
    dashboard_page()

elif st.session_state.page == "add_task":
    add_task_page()
elif st.session_state.page == "edit_task":
    edit_task_page()
elif st.session_state.page == "view_task":
    view_task_page()    

