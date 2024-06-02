POST http://localhost:5000/apply
{
    "yaml": "apiVersion: v1\\nkind: Pod\\nmetadata:\\n  name: mypod\\nspec:\\n  containers:\\n    - name: mycontainer\\n      image: nginx:latest\\n"
}
