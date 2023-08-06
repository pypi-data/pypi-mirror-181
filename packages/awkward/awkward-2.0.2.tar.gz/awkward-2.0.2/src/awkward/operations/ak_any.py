# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

np = ak._nplikes.NumpyMetadata.instance()


@ak._connect.numpy.implements("any")
def any(
    array,
    axis=None,
    *,
    keepdims=False,
    mask_identity=False,
    flatten_records=False,
    highlevel=True,
    behavior=None
):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        axis (None or int): If None, combine all values from the array into
            a single scalar result; if an int, group by that axis: `0` is the
            outermost, `1` is the first level of nested lists, etc., and
            negative `axis` counts from the innermost: `-1` is the innermost,
            `-2` is the next level up, etc.
        keepdims (bool): If False, this reducer decreases the number of
            dimensions by 1; if True, the reduced values are wrapped in a new
            length-1 dimension so that the result of this operation may be
            broadcasted with the original array.
        mask_identity (bool): If True, reducing over empty lists results in
            None (an option type); otherwise, reducing over empty lists
            results in the operation's identity.
        flatten_records (bool): If True, axis=None combines fields from different
            records; otherwise, records raise an error.
        highlevel (bool): If True, return an #ak.Array; otherwise, return
            a low-level #ak.contents.Content subclass.
        behavior (None or dict): Custom #ak.behavior for the output array, if
            high-level.

    Returns True in each group of elements from `array` (many types supported,
    including all Awkward Arrays and Records) if any values are True; False
    otherwise. Thus, it represents reduction over the "logical or" operation,
    whose identity is False (i.e. asking if there are any True values in an
    empty list results in False). This operation is the same as NumPy's
    [any](https://docs.scipy.org/doc/numpy/reference/generated/numpy.any.html)
    if all lists at a given dimension have the same length and no None values,
    but it generalizes to cases where they do not.

    See #ak.sum for a more complete description of nested list and missing
    value (None) handling in reducers.
    """
    with ak._errors.OperationErrorContext(
        "ak.any",
        dict(
            array=array,
            axis=axis,
            keepdims=keepdims,
            mask_identity=mask_identity,
            flatten_records=flatten_records,
            highlevel=highlevel,
            behavior=behavior,
        ),
    ):
        return _impl(
            array, axis, keepdims, mask_identity, flatten_records, highlevel, behavior
        )


def _impl(array, axis, keepdims, mask_identity, flatten_records, highlevel, behavior):
    layout = ak.operations.to_layout(array, allow_record=False, allow_other=False)
    backend = layout.backend
    reducer = ak._reducers.Any()

    if axis is None:
        if not backend.nplike.known_data or not backend.nplike.known_shape:

            def map(x):
                return ak._typetracer.UnknownScalar(
                    np.dtype(reducer.return_dtype(x.dtype))
                )

        else:

            def map(x):
                return backend.nplike.any(x.data)

        def reduce(xs):
            if len(xs) == 1:
                return xs[0]
            else:
                return backend.nplike.logical_or(xs[0], reduce(xs[1:]))

        return reduce(
            [
                map(x)
                for x in ak._do.completely_flatten(
                    layout, function_name="ak.any", flatten_records=flatten_records
                )
            ]
        )

    else:
        behavior = ak._util.behavior_of(array, behavior=behavior)
        out = ak._do.reduce(
            layout,
            reducer,
            axis=axis,
            mask=mask_identity,
            keepdims=keepdims,
            behavior=behavior,
        )
        if isinstance(out, (ak.contents.Content, ak.record.Record)):
            return ak._util.wrap(out, behavior, highlevel=highlevel)
        else:
            return out
