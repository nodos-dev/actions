import argparse
import json

# Custom function to handle both flag and 'true'/'false' string inputs
def str_to_bool(value):
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    raise argparse.ArgumentTypeError(f"Invalid value for a boolean argument: '{value}'. Use 'true' or 'false'.")

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process GitHub event-related arguments.")

    # Define the arguments (supporting both flags and 'true'/'false' string)
    parser.add_argument("--event-name", required=True, help="GitHub event name (e.g., push, workflow_dispatch)")
    parser.add_argument("--ref-name", required=True, help="GitHub ref name (e.g., branch or tag name)")
    parser.add_argument("--workflow-input-linux", type=str_to_bool, nargs="?", default=False, help="Enable Linux workflow input (true/false or flag)")
    parser.add_argument("--workflow-input-windows", type=str_to_bool, nargs="?", default=False, help="Enable Windows workflow input (true/false or flag)")
    parser.add_argument("--sign", type=str_to_bool, nargs="?", default=False, help="Enable signing (Windows only, true/false or flag)")
    parser.add_argument("--push-event-defaults", type=str, help="JSON string with push event defaults")
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract values
    event_name = args.event_name
    ref_name = args.ref_name
    workflow_input_linux = args.workflow_input_linux
    workflow_input_windows = args.workflow_input_windows
    sign = args.sign
    push_event_defaults = args.push_event_defaults

    # Initialize runner list
    runner_list = []

    if event_name in ["workflow_dispatch", "workflow_call"]:
        if workflow_input_linux:
            runner_list.append(["Linux"])
        if workflow_input_windows:
            win_labels = ["Windows"]
            if sign:
                win_labels.append("signer")
            runner_list.append(win_labels)
    elif event_name == "push":
        if push_event_defaults:
            push_event_defaults = json.loads(push_event_defaults)
            if push_event_defaults.get("linux", False):
                runner_list.append(["Linux"])
            if push_event_defaults.get("windows", False):
                win_labels = ["Windows"]
                if push_event_defaults.get("sign", False):
                    win_labels.append("signer")
                runner_list.append(win_labels)

    # Add default tags
    default_tags = ['self-hosted', ref_name]
    for runner in runner_list:
        runner.extend(default_tags)

    # Output the runner list
    print(str(runner_list))

if __name__ == "__main__":
    main()
