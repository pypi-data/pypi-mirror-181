# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

np = ak._nplikes.NumpyMetadata.instance()


@ak._connect.numpy.implements("argmin")
def argmin(
    array,
    axis=None,
    *,
    keepdims=False,
    mask_identity=True,
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

    Returns the index position of the minimum value in each group of elements
    from `array` (many types supported, including all Awkward Arrays and
    Records). The identity of minimization would be infinity, but argmin
    must return the position of the minimum element, which has no value for
    empty lists. Therefore, the identity should be masked: the argmin of
    an empty list is None. If `mask_identity=False`, the result would be `-1`,
    which is distinct from all valid index positions, but care should be taken
    that it is not misinterpreted as "the last element of the list."

    This operation is the same as NumPy's
    [argmin](https://docs.scipy.org/doc/numpy/reference/generated/numpy.argmin.html)
    if all lists at a given dimension have the same length and no None values,
    but it generalizes to cases where they do not.

    See #ak.sum for a more complete description of nested list and missing
    value (None) handling in reducers.

    See also #ak.nanargmin.
    """
    with ak._errors.OperationErrorContext(
        "ak.argmin",
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


@ak._connect.numpy.implements("nanargmin")
def nanargmin(
    array,
    axis=None,
    *,
    keepdims=False,
    mask_identity=True,
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
        mask_identity (bool): If True, reducing over empty lists results in
            None (an option type); otherwise, reducing over empty lists
            results in the operation's identity.
        flatten_records (bool): If True, axis=None combines fields from different
            records; otherwise, records raise an error.

    Like #ak.argmin, but treating NaN ("not a number") values as missing.

    Equivalent to

        ak.argmin(ak.nan_to_none(array))

    with all other arguments unchanged.

    See also #ak.argmin.
    """
    with ak._errors.OperationErrorContext(
        "ak.nanargmin",
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
        array = ak.operations.ak_nan_to_none._impl(array, False, None)

        return _impl(
            array, axis, keepdims, mask_identity, flatten_records, highlevel, behavior
        )


def _impl(array, axis, keepdims, mask_identity, flatten_records, highlevel, behavior):
    layout = ak.operations.to_layout(array, allow_record=False, allow_other=False)
    backend = layout.backend
    reducer = ak._reducers.ArgMin()

    if axis is None:
        if not backend.nplike.known_data or not backend.nplike.known_shape:
            return ak._typetracer.MaybeNone(
                ak._typetracer.UnknownScalar(np.dtype(reducer.return_dtype(None)))
            )

        layout = ak.operations.fill_none(layout, np.inf, axis=-1, highlevel=False)

        best_index = None
        best_value = None
        for tmp in ak._do.completely_flatten(
            layout, function_name="ak.argmin", flatten_records=flatten_records
        ):
            tmp = backend.nplike.asarray(tmp)
            if len(tmp) > 0:
                out = backend.nplike.argmin(tmp, axis=None)
                if best_index is None or tmp[out] < best_value:
                    best_index = out
                    best_value = tmp[out]
        return best_index

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
