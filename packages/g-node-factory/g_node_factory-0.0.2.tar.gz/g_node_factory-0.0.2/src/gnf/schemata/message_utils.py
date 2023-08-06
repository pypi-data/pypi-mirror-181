def confirm_to_alias(payload, to_alias):
    if not (payload["ToGNodeAlias"] == to_alias):
        print(
            f"Message ToGNodeAlias is {payload['ToGNodeAlias']} and this GNodeInstance has alias "
            f"{to_alias}. Ignoring message "
        )
        return False
    else:
        return True
