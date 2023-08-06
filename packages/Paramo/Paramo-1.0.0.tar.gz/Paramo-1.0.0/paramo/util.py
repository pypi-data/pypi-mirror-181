def unparse(query_list: dict) -> str:
    final = '?'

    for query in query_list:
        if query_list[query] is not None:
            final += f'{query}={query_list[query]}'

        else:
            final += query

        if not list(query_list)[-1] == query:
            final += '&'

    return final
