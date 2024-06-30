
#!/usr/bin/env bash

# A stub hook just to make sure that events are handled properly.

if [[ $1 == "--config" ]] ; then
  cat <<EOF
{
   "configVersion":"v1",
   "beforeHelm":1,
   "afterHelm":1,
   "afterDeleteHelm":1,
   "schedule":[
      {
         "crontab":"* * * * *",
         "allowFailure":true
      }
   ]
}
EOF
exit 0
else
echo "Updating runtime values for nginx module"
cat > $VALUES_JSON_PATCH_PATH <<EOF
$(python3 ./scripts/runtime-values-generator.py)
EOF
fi

binding=$(jq -r '.[0].binding' "${BINDING_CONTEXT_PATH}")

echo "Ran '${binding}' runtime values hook for nginx module"
