import os
import sys

# Args:
# --event-name: GitHub event name
# --ref-name: GitHub ref name
# --workflow-dispatch-input-linux
# --workflow-dispatch-input-windows
# --sign: Works only on Windows
# --push-event-defaults: JSON

event_name = None
ref_name = None
workflow_dispatch_input_linux = None
workflow_dispatch_input_windows = None
sign = None
push_event_defaults = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "--event-name":
        event_name = sys.argv[i + 1]
    elif sys.argv[i] == "--ref-name":
        ref_name = sys.argv[i + 1]
    elif sys.argv[i] == "--workflow-dispatch-input-linux":
        workflow_dispatch_input_linux = sys.argv[i + 1]
    elif sys.argv[i] == "--workflow-dispatch-input-windows":
        workflow_dispatch_input_windows = sys.argv[i + 1]
    elif sys.argv[i] == "--sign":
        sign = sys.argv[i + 1]
    elif sys.argv[i] == "--push-event-defaults":
        push_event_defaults = sys.argv[i + 1]

default_tags = ['self-hosted', ref_name]

runner_list = [] # E.g. [["self-hosted", "Linux", "dev"], ["self-hosted", "Windows", "dev"]]

if event_name == "workflow_dispatch":
    if workflow_dispatch_input_linux == "true":
        runner_list.append(default_tags + ["Linux"])
    if workflow_dispatch_input_windows == "true":
        win_labels = default_tags + ["Windows"]
        if sign == "true":
            win_labels.append("signer")
        runner_list.append(win_labels)
elif event_name == "push":
    if push_event_defaults:
        import json
        push_event_defaults = json.loads(push_event_defaults)
        # E.g.: {"linux": true, "windows": true, "sign": true}
        if push_event_defaults["linux"] or push_event_defaults["linux"] == "true":
            runner_list.append(default_tags + ["Linux"])
        if push_event_defaults["windows"] or push_event_defaults["windows"] == "true":
            win_labels = default_tags + ["Windows"]
            if push_event_defaults["sign"] or push_event_defaults["sign"] == "true":
                win_labels.append("signer")
            runner_list.append(win_labels)

print(runner_list)