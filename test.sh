cat > $CONFIG_VALUES_JSON_PATCH_PATH <<EOF
    [{"op":"add", "path":"/someModule/param3", "value":"newValue"}]
EOF