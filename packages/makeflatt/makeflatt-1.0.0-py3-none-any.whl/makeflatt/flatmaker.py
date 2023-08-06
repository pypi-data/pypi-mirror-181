class NotADictionaryException(Exception):
    def __init__(self, data) -> None:
        super().__init__(f"Expected a dictionary, got {type(data)}")


class FlattMaker:
    def __init__(self, sep=".") -> None:
        self.sep = sep

    def _make_flat(
        self, data: dict, parent_key: str = "", make_list_flatten: bool = False
    ):
        items = []
        for k, v in data.items():
            new_key = parent_key + self.sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    self._make_flat(
                        v, new_key, make_list_flatten=make_list_flatten
                    ).items()
                )
            elif isinstance(v, list) and make_list_flatten:
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        items.extend(
                            self._make_flat(
                                v[i],
                                new_key + self.sep + str(i),
                                make_list_flatten=make_list_flatten,
                            ).items()
                        )
                    else:
                        items.append((new_key + self.sep + str(i), v[i]))
            else:
                items.append((new_key, v))
        return dict(items)

    def apply(self, data: dict):
        if isinstance(data, dict):
            return self._make_flat(data)

        raise NotADictionaryException(data)

    def deep_apply(self, data: dict):
        if isinstance(data, dict):
            return self._make_flat(data, make_list_flatten=True)

        raise NotADictionaryException(data)
