from graphql.language.ast import Document


def fetch_operation_from_ast(ast: Document, operation_name: str):
    results = [[selection for selection in definition.selection_set.selections if selection.name.value == operation_name]
               for definition in ast.definitions]
    if not len(results) == 1 or not len(results[0]) == 1:
        return None
    return results[0][0]


def get_subselection(base_selection, name, parent_name):
    sub_selections = [selection for selection in base_selection.selection_set.selections if any(
        [sub_selection.name.value == name and selection.name.value == parent_name for sub_selection in selection.selection_set.selections])]
    return sub_selections
