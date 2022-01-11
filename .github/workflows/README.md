## Naming rule
```
[EVENT] CONTENT
```

## Workflows
- `[Push|Dispatch] Build dev`
    - EVENT
        - When code is pushed to master
            - (triggered by `[Push] Sync CI`)
        - When the workflow is manually triggered
    - CONTENT
        - Build code and push docker image to pyengine
- `[Dispatch] Release`
    - EVENT
        - When the workflow is manually triggered
    - CONTENT
        - Build code and push docker image to pyengine and spaceone
- `[Push] Sync CI`
    - EVENT
        - When code is pushed to master
            - (trigger `[Push] Build dev`)
    - CONTENT
        - Get workflows from actions and Trigger `[Push|Dispatch] Build dev`
- `[Dispatch] Sync CI`
    - EVENT
        - When the workflow is manually triggered
    - CONTENT
        - Just get workflows from actions
- `[PR] Review (TODO)`

## Scenario
- Release: `[Dispatch] Release`
- Build Dev (Push): `[Push] Sync CI` -> `[Push|Dispatch] Build dev`
- Build Dev (Dispatch): `[Push|Dispatch] Build dev`
- Update workflows: `[Dispatch] Sync CI`
