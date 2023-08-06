
import numpy as np
import json
from html import escape
from typing import List, Dict # TODO: add to every funtion or method the appropriate typing e.g. index: Dict[str|int,List[str|int]] | None = None. After that use Mypy
from functools import reduce
from itertools import product
from .utils import _format_bytes, css
from .setting import settings

#TODO: add datetime option to dimnesions
#TODO: implement test module
#TODO: implement logger
#TODO: add corresponding message to every assertion
#TODO: Add to every function or method a docstrings with examples
#TODO: create Materials Mk Docs
#TODO: Long.value !=, ==, >, < 
#TODO: Improve save/load an Array object

class Long:
    def __init__(self, index:Dict[str, np.ndarray|List[str|int]], value:np.ndarray|List[float]) -> None:
        # Assertion with value
        assert isinstance(value, (np.ndarray, list, float))
        if isinstance(value, np.ndarray):
            assert issubclass(value.dtype.type, float)
            if value.ndim == 0:
                value = value.reshape((value.size,))
        elif isinstance(value, float):
            value = np.array([value], dtype=float)
        else:
            assert all([isinstance(elem, (float,int,np.integer)) for elem in value])
            value = np.array(value, dtype=float)
        assert value.ndim == 1
        # Assertion with index
        assert isinstance(index, dict)
        assert all([isinstance(index[dim], (np.ndarray,list)) for dim in index])
        for dim in index:
            if isinstance(index[dim], list):
                if all(isinstance(elem, str) for elem in index[dim]):
                    index[dim] = np.array(index[dim], dtype=np.object_)
                elif all(isinstance(elem, int) for elem in index[dim]):
                    index[dim] = np.array(index[dim], dtype=int)
        assert all([index[dim].ndim == 1 for dim in index])
        assert all([index[dim].size == value.size for dim in index])
        assert 'value' not in index, "'value' can not be a dimension name as it is reserved"
        assert all([isinstance(dim, str) for dim in index])

        self._value = value
        self._index = index
        self._dims = list(self._index)
        self._dtype = {dim: index[dim].dtype.type for dim in self._dims}

        self.rows_display = 16
        self.decimals_display = 2
        self.oneshot_display = False

    def _repr_html_(self) -> str:
        long_nbytes = _format_bytes(sum([self._index[dim].nbytes for dim in self._index] + [self._value.nbytes]))
        dims = self.dims
        items = self._value.size

        if items > self.rows_display:
            short = False
            if self.oneshot_display:
                rows = self.rows_display
            else:
                rows = int(self.rows_display/2)
        else:
            short = True
            rows = items

        columns = dims + ['value']
        html = [f"{css}"]
        html += ['<h3>Long</h3>',
                '<table>',
                f'<tr><th>Object size</th><td>{long_nbytes}</td></tr>',
                f'<tr><th>Dimensions</th><td>{dims}</td></tr>',
                '<!-- SHAPE -->',
                f'<tr><th>Rows</th><td>{items}</td></tr>',
                '</table>']
        html += ["<!-- COORDS -->"]
        html += [f"<details>"]
        html += [f'<table><summary><div class="tooltip"> Show data <small>[default: 16 rows, 2 decimals]</small>']
        html += [f'<!-- A --><span class="tooltiptext tooltip-top">To change default values:<br> obj.rows_display = Int val<br>obj.decimals_display = Int val<br>obj.self.oneshot_display = False<!-- Z -->']
        html += ['</span></div></summary><tr><th>']
        html += [f"<th>{j}" for j in columns]
   
        for i in range(rows):
            html.append(f"<tr><th><b>{i}</b>")
            for j,v in self.items():
                val = v[i]
                html.append("<td>")
                html.append(escape(f"{val:.{self.decimals_display}f}" if issubclass(v.dtype.type, np.float_) else f"{val}"))

        if not self.oneshot_display:
            if not short:
                html.append("<tr><th>")
                for _ in range(len(dims)+1):
                    html.append("<td>...")
                for i in range(items-rows,items,1):
                    html.append(f"<tr><th><b>{i}</b>")
                    for j,v in self.items():
                        val = v[i]
                        html.append("<td>")
                        html.append(escape(f"{val:.{self.decimals_display}f}" if issubclass(v.dtype.type, np.float_) else f"{val}"))
        html.append("</table></details>")
        return "".join(html)

    @property
    def index(self):
        assert set(self.dims) == set(self._index.keys()), "dims names must match with index names" 
        return {dim:self._index[dim] for dim in self.dims}

    @property
    def value(self):
        return self._value.copy()

    @property
    def dims(self):
        return self._dims[:]

    @property
    def dtype(self):
        return self._dtype

    @property
    def size(self):
        return self.value.size

    @property
    def ndim(self):
        return len(self.index)

    def insert(self, **kwargs):
        assert all([dim not in self.dims for dim in kwargs])
        assert all([isinstance(value, (str, int, dict)) for value in kwargs.values()])
        for value in kwargs.values():
            if isinstance(value, dict):
                assert len(value) == 1
                existing_dim = next(iter(value))
                assert isinstance(existing_dim, (str, int))
                assert existing_dim in self.dims
                assert isinstance(value[existing_dim], dict)
                new_dim_items = list(value[existing_dim])
                new_dim_items_set = set(new_dim_items)
                assert set(np.unique(self.index[existing_dim])).issubset(new_dim_items_set)
                assert len(new_dim_items) == len(new_dim_items_set) # mapping has unique keys

        index = {}
        for new_dim in kwargs:
            value = kwargs[new_dim]
            if isinstance(value, str):
                idxarray = np.empty(self.size, dtype=np.object_)
                idxarray[:] = value
            elif isinstance(value, int):
                idxarray = np.empty(self.size, dtype=np.integer)
                idxarray[:] = value
            elif isinstance(value, dict):
                existing_dim = next(iter(value))
                mapping_dict = value[existing_dim]
                existing_dim_items = self.index[existing_dim]
                k = np.array(list(mapping_dict)) # This must be unique
                v = np.array(list(mapping_dict.values())) # This not necessary unique
                idxarray = np.array(v)[np.searchsorted(k, existing_dim_items, sorter=list(range(k.size)))]
            index[new_dim] = idxarray

        for dim in self.index:
            index[dim] = self.index[dim]

        return Long(index=index, value=self.value)
    
    def rename(self, **kwargs):
        assert all([odim in self.dims for odim in kwargs])
        assert all([ndim not in self.dims for ndim in kwargs.values()])
        index = {}
        for dim in self.dims:
            if dim in kwargs:
                index[kwargs[dim]] = self._index[dim]
            else:
                index[dim] = self._index[dim]
        return Long(index=index, value=self._value)

    def drop(self, dims:str|list):
        assert isinstance(dims, (str, list))
        index = {}
        if isinstance(dims, str):
            assert dims in self.dims
            for dim in self.dims:
                if dim != dims:
                    index[dim] = self._index[dim]
            item_tuples = list(zip(*index.values()))
            assert len(set(item_tuples)) == len(item_tuples), f"Index items per row must be unique. By removing {dims} leads the existence of repeated indexes"
            return Long(index=index, value=self._value)
        elif isinstance(dims, list):
            assert all([dim in self.dims for dim in dims])
            for dim in self.dims:
                if dim not in dims:
                    index[dim] = self._index[dim]
            item_tuples = list(zip(*index.values()))
            assert len(set(item_tuples)) == len(item_tuples), f"Index items per row must be unique. By removing {dims} leads the existence of repeated indexes"
            return Long(index=index, value=self._value)
        
    def items(self):
        dc = dict(**self.index)
        dc.update(dict(value=self._value))
        for k,v in dc.items():
            yield (k,v)

    def __getitem__(self, item):
        assert isinstance(item, (str, int, list, np.ndarray, slice, tuple))
        if isinstance(item, int):
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, list):
            item = np.array(item, dtype=int)
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, np.ndarray):
            assert issubclass(item.dtype.type, np.integer) or issubclass(item.dtype.type, np.bool_)
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        # Go over the index of the numpy array
        elif isinstance(item, slice):
            return Long(index={dim:self._index[dim][item] for dim in self.dims}, value=self._value[item])
        elif isinstance(item, str):
            assert item in self.dims
            return self._index[item]
        elif isinstance(item, tuple):
            assert len(item) == 2
            if isinstance(item[0], (str, int)):
                dim = item[0]
                condition = item[1]
                assert dim in self.dims
                assert isinstance(condition, (list, np.ndarray, slice))
                index_items_on_dim = self._index[dim]
                # Go over the elements of the numpy array
                if isinstance(condition, (list,np.ndarray)):
                    mask = np.isin(index_items_on_dim, condition)
                    return Long(index={dim_:self._index[dim_][mask] for dim_ in self.dims}, value=self._value[mask])
                # only works if elements of the numpy array are integers
                elif isinstance(condition, slice):
                    assert issubclass(index_items_on_dim.dtype.type, np.integer)
                    start = condition.start or 0
                    stop = condition.stop or self._value.size
                    step = condition.step or 1
                    arange_condition = np.arange(start,stop,step)
                    mask = np.isin(index_items_on_dim, arange_condition)
                    return Long(index={dim_:self._index[dim_][mask] for dim_ in self.dims}, value=self._value[mask])
            elif isinstance(item[0], list):
                reorder = item[0]
                assert set(self.dims) == set(reorder)
                assert isinstance(item[1], slice)
                condition = item[1]
                start = condition.start or 0
                stop = condition.stop or self._value.size
                step = condition.step or 1
                arange_condition = np.arange(start,stop,step)
                return Long(index={dim_:self._index[dim_][arange_condition] for dim_ in reorder}, value=self._value[arange_condition])
            # TODO: Implement slice of datetime

    def __eq__(self, __o: object):
        if np.isnan(__o):
            return np.isnan(self._value)
        elif np.isinf(__o):
            return np.isinf(self._value)
        elif isinstance(__o, np.generic):
            raise Exception("np.ndarray not supported yet")
        elif isinstance(__o, (int,float)):
            return self._value == __o
        elif isinstance(__o, Long):
            if not tuple(self.dims) == tuple(__o.dims):
                return False
            return all([np.array_equal(own[1],other[1]) for own, other in zip(self.items(),__o.items())])
        else:
            raise Exception(f"{type(__o)} not supported yet")

    def __ne__(self, __o: object):
        if np.isnan(__o):
            return ~np.isnan(self._value)
        elif np.isinf(__o):
            return ~np.isinf(self._value)
        elif isinstance(__o, np.generic):
            raise Exception("np.ndarray not supported yet")
        elif isinstance(__o, (int,float)):
            return self._value != __o
        else:
            raise Exception(f"{type(__o)} not supported yet")


class Array:
    """
    A class for labelled multidimensional arrays.
    """
    def __init__(self, data:tuple|Long|None=None, coords:dict|None=None, keep_zeros:bool=False):
        '''
        Initialize a karray.
        
        Args:
            data: must be a tuple of index,value or a Long object.
            coords (dict[key:str, values:list|np.ndarray[str|int|datetime64]): dictionary with all possible coordinates.
            keep_zeros (bool): if False, it removes all zeros from value in order to keep small object size. Default: False.

            data could be:
            - tuple index,value: index (dict[keys:str|int, values:list|np.ndarray[int|str|datetime64]): keys are dim names, values are 1d array of dim coordinates or list.
                                 value (np.ndarray|list): 1d array of float.
            - long (Long) is a Long instance

            A rule for the order of the array dimensions> coords keys sets dims order, otherwise index sets the order of dims. Both are subject to order list if not None.

        Example:
            >>> import karray as ka
            >>> import numpy as np
            First example
            >>> index = {'x':[2,5], 'y':[1,4]}
            >>> value = [3.0,6.0]
            >>> ar = ka.Array(data = (index, value), coords = {'x':[2,5,7], 'y':[1,4,8]}
            Second example
            >>> long = Long(index=index, value=value)
            >>> ar = ka.Array(data = long, coords = {'x':[2,5,7], 'y':[1,4,8]}
            Third example
            >>> long_format_2darray = np.array([[2,1,3.0],[5,4,6.0]]) # First two columns are dimensions, last column is value.
            >>> long = ka.numpy_to_long(array=long_format_2darray, dims=['x','y'])
            >>> ar = ka.Array(data = long, coords = {'x':[2,5,7], 'y':[1,4,8]})

        '''
        self.__dict__["_repo"] = {}
        self.long = None
        self.coords = None
        self.attr_constructor(keep_zeros=keep_zeros, **self.check_input(data, coords))
        self.keep_zeros = keep_zeros
        order = self._order_with_preference(self.dims, settings.order)
        if tuple(order) == tuple(self.dims):
            pass
        else:
            self.long = self.long[order,:]
            self.coords = {dim: self.coords[dim] for dim in order}
        return None

    def check_input(self, data, coords):
        assert isinstance(data, (Long, tuple, type(None)))
        if isinstance(data, Long):
            long:Long|None = data
            index:dict|None = None
            value:np.ndarray|None = None
        elif isinstance(data, tuple):
            long:Long|None = None
            index:dict|None = data[0]
            value:np.ndarray|None = data[1]
        else:
            long:Long|None = None
            index:dict|None = None
            value:np.ndarray|None = None
            assert coords is not None
        # TODO: Add here the assertions indicated below.
        if coords is not None:
            assert isinstance(coords, dict)
            if long is not None:
                assert set(long.dims) == set(list(coords))
            elif index is not None:
                assert set(list(index)) == set(list(coords))
            cdims = list(coords)
            for dim in cdims:
                assert isinstance(dim, (str, int))
                if isinstance(coords[dim], list):
                    dtype = np.integer if isinstance(coords[dim][0], int) else np.object_
                    coords[dim] = np.sort(np.array(coords[dim], dtype=dtype))

                assert isinstance(coords[dim], np.ndarray)
                assert issubclass(coords[dim].dtype.type, np.object_) or issubclass(coords[dim].dtype.type, np.integer)
                assert coords[dim].ndim == 1
                assert coords[dim].size == np.unique(coords[dim]).size, f"coords elements of dim '{dim}' must be unique. {coords[dim].size=}, {np.unique(coords[dim]).size=}"
        return dict(long=long, index=index, value=value, coords=coords)

    def attr_constructor(self, long, index, value, coords, keep_zeros:bool=False):
        # Check input has several assertions, compare and modify accordingly
        # TODO: Noticed that coords dims could be str or int, while index in Long class can only be str. We must fix everywhere that coords keys -> dimension can only be str!
        if long is not None:
            if coords is not None: # TODO: Assertion: set(coords.keys()) == set(long.dims). Assertion long.index arrays are subset of coords values
                if len(coords) == 0:
                    assert long.ndim == 0
                    self.coords = coords
                else:
                    long = long[list(coords),:]
                    self.coords = {dim:np.sort(coords[dim]) for dim in coords}
            else:
                self.coords = {dim:np.sort(np.unique(long.index[dim])) for dim in long.dims}
            self.long = long if keep_zeros else long[long != 0.0]
        elif index is not None: # TODO: Index is not None -> Assertion: index is a dictionary and values np.ndarray[int|str|datetime64].
            if value is None:
                raise Exception("If 'index' is not None, then 'value' must be provided. Currently 'value' is None")
            else: # TODO: assertion that values is an np.ndarray of floats
                if coords is not None: # TODO: Assertion for key and values type. Assertion: array elements must be unique. Assertion: unique elements of index must be a subset of coords elements
                    assert set(coords) == set(index)
                    coords = {dim:np.sort(coords[dim]) for dim in coords}
                    index = {dim:index[dim] for dim in coords}
                else:
                    coords = {dim:np.sort(np.unique(index[dim])) for dim in index}
                self.coords = coords
                long = Long(index=index, value=value)
                self.long = long if keep_zeros else long[long != 0.0]
        else:
            if value is None:
                assert value is None and index is None and coords is not None
                self.coords = {dim:np.sort(coords[dim]) for dim in coords}
                dtypes = {dim: self.coords[dim].dtype.type for dim in coords}
                # Create an empty Long object (It will lead to a dense array of zeros)
                if len(coords) == 0:
                    self.long = Long(index={}, value= np.array([], dtype=float))
                else:
                    self.long = Long(index={dim: np.array([], dtype=dtypes[dim]) for dim in coords}, value= np.array([], dtype=float))
            else:
                raise Exception("If 'value' is not None, then 'index' must be provided. Currently 'index' is None")
        return None

    def __repr__(self):
        return f"Karray.Array(data, coords)"

    def _repr_html_(self):
        html = ['<details><table><summary><div class="tooltip"> Show unique coords</div></summary>']
        html.append("<tr><th>Dimension<th>Length<th>Type<th>Items")
        for dim in self.coords:
            html.append(f"<tr><th><b>{dim}</b><td>")
            html.append(escape(f"{len(self.coords[dim])}"))
            html.append(f"<td>{self.coords[dim].dtype}<td>")
            html.append(f'<details><summary><div class="tooltip">show details</div></summary>')
            html.append(escape(f"{self.coords[dim]}"))
        html.append("</table></details>")
        script = ''.join(html)
        shape = f"<tr><th>Shape</th><td>{self.shape}</td></tr>"
        return self.long._repr_html_().replace('Long','[k]array') \
                                      .replace('<!-- COORDS -->',script) \
                                      .replace('<!-- SHAPE -->',shape) \
                                      .replace('<!-- A -->','<!-- ') \
                                      .replace('<!-- Z -->',' -->')

    def __setattr__(self, name, value):
        self._repo[name] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name) # ipython requirement for repr_html
        else:
            return self._repo[name]

    def _shape(self, coords):
        return [coords[dim].size for dim in coords]

    @property
    def shape(self):
        return self._shape(self.coords)


    def _capacity(self, coords):
        return int(np.prod(self._shape(coords)))

    @property
    def capacity(self):
        return self._capacity(self.coords)

    @property
    def dims(self):
        return self.long.dims

    @property
    def cindex(self):
        return list(zip(*self.long.index.values()))

    @property
    def dindex(self):
        return self._dindex(self.coords)

    def _dindex(self, coords):
        return list(product(*list(coords.values()))) # TODO: compare list or sorted

    def _dense(self, coords):
        if self.long.ndim == 0:
            return self.long.value
        long_stack = np.vstack([np.searchsorted(coords[dim], self.long._index[dim]) for dim in coords])
        indexes = np.ravel_multi_index(long_stack, self._shape(coords))
        dense = np.zeros((self._capacity(coords),), dtype=float)
        dense[indexes] = self.long.value
        return dense.reshape(self._shape(coords))
    
    def dense(self):
        return self._dense(self.coords)

    @staticmethod
    def _reorder(self_long, self_coords, reorder=None):
        assert reorder is not None, "order must be provided"
        assert set(reorder) == set(self_long.dims), "order must be equal to self.dims, the order can be different, though"
        if tuple(self_long.dims) == tuple(reorder):
            return dict(data=self_long, coords=self_coords)
        coords = {k:self_coords[k] for k in reorder}
        long = self_long[reorder,:]
        return dict(data=long, coords=coords)

    def reorder(self, reorder=None):
        return Array(keep_zeros=self.keep_zeros,**self._reorder(self.long, self.coords, reorder))

    @staticmethod
    def _order_with_preference(dims:list, preferred_order:list=None):
        if preferred_order is None:
            return dims
        else:
            ordered = []
            unourdered = dims[:]
            for dim in preferred_order:
                if dim in unourdered:
                    ordered.append(dim)
                    unourdered.remove(dim)
            ordered.extend(unourdered)
            return ordered

    def _union_dims(self, other, preferred_order: list = None):
        if set(self.dims) == set(other.dims):
            return self._order_with_preference(self.dims, preferred_order)
        elif len(self.dims) == 0 or len(other.dims) == 0:
            for obj in [self,other]:
                if len(obj.dims) > 0:
                    dims = obj.dims
            return self._order_with_preference(dims, preferred_order)
        elif len(set(self.dims).symmetric_difference(set(other.dims))) > 0:
            common_dims = set(self.dims).intersection(set(other.dims))
            assert len(common_dims) > 0, "At least one dimension must be common"
            uncommon_dims = set(self.dims).symmetric_difference(set(other.dims))
            uncommon_self = [dim for dim in self.dims if dim in uncommon_dims]
            uncommon_other = [dim for dim in other.dims if dim in uncommon_dims]
            assert not all([len(uncommon_self) > 0, len(uncommon_other) > 0]), f"Uncommon dims must be in only one array. {uncommon_self=} {uncommon_other=}"
            unordered = list(set(self.dims).union(set(other.dims)))
            semi_ordered = self._order_with_preference(unordered, preferred_order)
            ordered_common = []
            if preferred_order is None:
                return list(common_dims) + list(uncommon_dims)
            else:
                for dim in preferred_order:
                    if dim in common_dims:
                        ordered_common.append(dim)
                        common_dims.remove(dim)
                ordered_common.extend(common_dims)
                for dim in ordered_common:
                    if dim in semi_ordered:
                        semi_ordered.remove(dim)
                ordered =  ordered_common + semi_ordered
                return ordered

    def _union_coords(self, other, uniondims):
        coords = {}
        for dim in uniondims:
            if dim in self.coords:
                if dim in other.coords:
                    coords[dim] = np.sort(np.union1d(self.coords[dim], other.coords[dim]))
                else:
                    coords[dim] = self.coords[dim]
            elif dim in other.coords:
                coords[dim] = other.coords[dim]
            else:
                raise Exception(f"Dimension {dim} not found in either arrays")
        return coords

    def _get_inv_dense(self, uniondims, unioncoords):
        self_dims = [d for d in uniondims if d in self.dims]
        self_coords = {d:unioncoords[d] for d in self_dims}
        self_inv_dense = self._dense(self_coords).T
        return self_inv_dense

    def _pre_operation_with_array(self, other):
        uniondims = self._union_dims(other, preferred_order=settings.order)
        unioncoords = self._union_coords(other, uniondims)
        self_inv_dense = self._get_inv_dense(uniondims, unioncoords)
        other_inv_dense = other._get_inv_dense(uniondims, unioncoords)
        return self_inv_dense, other_inv_dense, unioncoords

    def _pre_operation_with_number(self):
        return self._dense(self.coords).T

    def _post_operation(self, resulting_dense, coords):
        dense = resulting_dense.T
        if len(coords) == 0:
            return Array(keep_zeros=self.keep_zeros, data=({},dense), coords=coords)
        arrays = np.unravel_index(np.arange(self._capacity(coords)), self._shape(coords))
        index = {dim:coords[dim][idx] for dim, idx in zip(coords,arrays)}
        long = Long(index=index, value=dense.reshape(dense.size))
        if not self.keep_zeros:
            long = long[long != 0]
        return Array(keep_zeros=self.keep_zeros, data=long, coords=coords)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = self_dense + other
            return self._post_operation(resulting_dense, self.coords)
        elif isinstance(other, Array):
            self_dense, other_dense, coords = self._pre_operation_with_array(other)

            resulting_dense = self_dense + other_dense

            return self._post_operation(resulting_dense, coords)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = self_dense * other
            return self._post_operation(resulting_dense, self.coords)
        elif isinstance(other, Array):
            self_dense, other_dense, coords = self._pre_operation_with_array(other)

            resulting_dense = self_dense * other_dense
            
            return self._post_operation(resulting_dense, coords)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = self_dense - other
            return self._post_operation(resulting_dense, self.coords)
        elif isinstance(other, Array):
            self_dense, other_dense, coords = self._pre_operation_with_array(other)

            resulting_dense = self_dense - other_dense
            
            return self._post_operation(resulting_dense, coords)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = self_dense / other
            return self._post_operation(resulting_dense, self.coords)
        elif isinstance(other, Array):
            self_dense, other_dense, coords = self._pre_operation_with_array(other)
            # resulting_dense = self_dense / other_dense

            # Avoid zero division warning
            # Method 1
            # resulting_dense = np.divide(self_dense, other_dense, out=np.zeros(self_dense.shape, dtype=float), where=other_dense!=0)
            # Method 2
            # mask = other_dense != 0.0
            # resulting_dense = self_dense.copy()
            # np.divide(self_dense, other_dense, out=resulting_dense, where=mask)
            # Method 3
            resulting_dense = np.zeros_like(self_dense)
            np.divide(self_dense, other_dense, out=resulting_dense, where=~np.isclose(other_dense,np.zeros_like(other_dense)))
            return self._post_operation(resulting_dense, coords)

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = other + self_dense
            return self._post_operation(resulting_dense, self.coords)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = other * self_dense
            return self._post_operation(resulting_dense, self.coords)

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = other - self_dense
            return self._post_operation(resulting_dense, self.coords)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            self_dense = self._pre_operation_with_number()
            resulting_dense = other / self_dense
            return self._post_operation(resulting_dense, self.coords)

    def __neg__(self):
        self_dense = self._pre_operation_with_number()
        resulting_dense = -self_dense
        return self._post_operation(resulting_dense, self.coords)

    def __pos__(self):
        self_dense = self._pre_operation_with_number()
        resulting_dense = +self_dense
        return self._post_operation(resulting_dense, self.coords)

    def to_dataframe(self):
        import pandas as pd
        if self.long.ndim == 0:
            return pd.DataFrame(pd.Series(self._dense(self.coords).reshape(-1), index=[0], name='value'))
        else:
            mi = pd.MultiIndex.from_tuples(self.dindex, names=self.dims)
            return pd.DataFrame(pd.Series(self._dense(self.coords).reshape(-1), index=mi, name='value'))

    def to_arrow(self):
        import pyarrow as pa
        import pandas as pd
        table = pa.Table.from_pandas(pd.DataFrame({k:v for k,v in self.long.items()}))
        existing_meta = table.schema.metadata
        custom_meta_key = 'karray'
        custom_metadata = {}
        attr = ['coords']
        for k,v in self._repo.items():
            if k in attr:
                if 'coords' == k:
                    v = {dim:v[dim].tolist() for dim in v}
                custom_metadata[k] = v
        custom_meta_json = json.dumps(custom_metadata)
        existing_meta = table.schema.metadata
        combined_meta = {custom_meta_key.encode() : custom_meta_json.encode(),**existing_meta}
        return table.replace_schema_metadata(combined_meta)

    def to_feather(self, path):
        import pyarrow.feather as ft
        table = self.to_arrow()
        ft.write_feather(table, path)
        return None

    def shrink(self, **kwargs):
        assert all([kw in self.coords for kw in kwargs]), "Selected dimension must be in coords"
        assert all([isinstance(val, list) for val in kwargs.values()]), "Keeping elements must be contained in lists"
        assert all([set(kwargs[kw]).issubset(self.coords[kw]) for kw in kwargs]), "All keeping elements must be included of coords"
        assert all([len(set(kwargs[kw])) == len(kwargs[kw]) for kw in kwargs]), "Keeping elements in list must be unique"
        # removing elements from coords dictionary
        new_coords = {}
        for dim in self.coords:
            if dim in kwargs:
                new_coords[dim] = np.sort(np.array(kwargs[dim], dtype=np.object_))
            else:
                new_coords[dim] = self.coords[dim]
        long = self.long
        for dim in self.dims:
            if dim in kwargs:
                long = long[dim, kwargs[dim]]
        return Array(keep_zeros=self.keep_zeros, data=long, coords=new_coords)

    def add_elem(self, **kwargs):
        coords = {}
        for dim in kwargs:
            assert dim in self.dims, f'dim: {dim} must exist in self.dims: {self.dims}'
        for dim in self.coords:
            if dim in kwargs:
                coords[dim] = np.sort(np.unique(np.hstack(self.coords[dim], np.array(kwargs[dim], dtype=np.object_))))
            else:
                coords[dim] = self.coords[dim]
        return Array(keep_zeros=self.keep_zeros, data=self.long, coords=coords)

    def reduce(self, dim:str, aggfunc:str='sum'):
        '''
        aggfunc in ['sum','mul','mean']. defult 'sum'
        '''
        assert dim in self.dims, f"dim {dim} not in self.dims: {self.dims}"
        if aggfunc == 'sum':
            dense = np.add.reduce(self._dense(self.coords), axis=self.dims.index(dim))
        elif aggfunc == 'mul':
            dense = np.multiply.reduce(self._dense(self.coords), axis=self.dims.index(dim))
        elif aggfunc == 'mean':
            dense = np.average(self._dense(self.coords), axis=self.dims.index(dim))
        dims = [d for d in self.dims if d != dim]
        coords = {k:v for k,v in self.coords.items() if k in dims}
        return self._post_operation(dense.T, coords)

    def insert(self, **kwargs):
        coords = {}
        for new_dim in kwargs:
            assert new_dim not in self.dims
            value = kwargs[new_dim]
            if isinstance(value, str):
                coords[new_dim] = np.array([value], dtype=np.object_)
            elif isinstance(value, int):
                coords[new_dim] = np.array([value], dtype=int)
            elif isinstance(value, dict):
                assert len(value) == 1
                existing_dim = next(iter(value))
                assert isinstance(existing_dim, (str, int))
                assert existing_dim in self.dims
                assert isinstance(value[existing_dim], dict)
                new_dim_items_set = set(value[existing_dim])
                assert set(self.coords[existing_dim])== new_dim_items_set, f"All items in the mapping dict associated with '{new_dim}' and '{existing_dim}' must be included in .coords['{existing_dim}']"
                assert len(value[existing_dim]) == len(new_dim_items_set), f"There are duplicate items in the mapping dict associated with '{new_dim}' and '{existing_dim}'" # mapping has unique keys
                new_items = set(value[existing_dim].values())
                assert all([isinstance(elem, str) for elem in new_items]) or all([isinstance(elem, int) for elem in new_items]) # TODO: future include datetime64, Assertion: inlude this assertion __init__ for coords
                if all([isinstance(elem, str) for elem in new_items]):
                    coords[new_dim] = np.array(sorted(new_items), dtype=np.object_)
                elif all([isinstance(elem, int) for elem in new_items]):
                    coords[new_dim] = np.array(sorted(new_items), dtype=int)
        for dim in self.coords:
            coords[dim] = self.coords[dim]
        long = self.long.insert(**kwargs)
        return Array(keep_zeros=self.keep_zeros, data=long, coords=coords)

    def add_dim(self, **kwargs):
        return self.insert(**kwargs)
        
    def rename(self, **kwargs):
        for olddim, newdim in kwargs.items():
            assert olddim in self.dims, f"Dimension {olddim} must be in dims {self.dims}"
            assert newdim not in self.dims, f"Dimension {newdim} must not be in dims {self.dims}"
        coords = {}
        for dim, elems in self.coords.items():
            if dim in kwargs:
                coords[kwargs[dim]] = elems
            else:
                coords[dim] = elems
        dims = self.dims[:]
        for dim in kwargs:
            dims[dims.index(dim)] = kwargs[dim]
        long = self.long.rename(**kwargs)
        return Array(keep_zeros=self.keep_zeros, data=long, coords=coords)
    
    def dropna(self, infinite=True):
        long = self.long
        long = long[long != np.nan]
        if infinite:
            long = long[long != np.inf]
            long = long[long != -np.inf]
        return Array(long,self.coords)


def concat(arrays:list, keep_zeros=False):
    dims = arrays[0].dims[:]
    assert all([isinstance(arr, Array) for arr in arrays]), "All list items must be karray.array"
    assert all([set(arr.dims) == set(dims) for arr in arrays]), "All array must have the same dimensions"
    index = {dim:[] for dim in dims}
    value = []
    [index[dim].append(arr.long.index[dim]) for arr in arrays for dim in arr.dims]
    index = {dim:np.hstack(index[dim]) for dim in dims}
    [value.append(arr.long.value) for arr in arrays]
    value = np.hstack(value)
    coords = reduce(lambda x,y: Array(keep_zeros=keep_zeros, data=x.long, coords=x._union_coords(y,x.dims)), arrays).coords
    return Array(keep_zeros=keep_zeros, data=(index,value), coords=coords)

def numpy_to_long(array:np.ndarray, dims:list) -> Long:
    assert isinstance(array, np.ndarray)
    assert isinstance(dims, list)
    assert array.ndim == 2, "Array must be a 2 dimensions array"
    assert len(dims) + 1 == len(array.T), f"Numpy array must contain {len(dims) + 1} columns"
    value = array.T[len(dims)]
    _index = {dim:arr for dim, arr in zip(dims, array.T[0:len(dims)])}
    _value = value if issubclass(value.dtype.type, float) else value.astype(float)
    return Long(_index, _value)

def from_feather(path, with_table=False, keep_zeros=False):
    import pyarrow.feather as ft
    restored_table = ft.read_table(path)
    custom_meta_key = 'karray'
    restored_meta_json = restored_table.schema.metadata[custom_meta_key.encode()]
    restored_meta = json.loads(restored_meta_json)
    long = numpy_to_long(restored_table.to_pandas().to_numpy(), list(restored_meta['coords']))
    if with_table:
        return Array(keep_zeros=keep_zeros, data=long, coords= restored_meta['coords']), restored_table
    return Array(keep_zeros=keep_zeros, data=long, coords= restored_meta['coords'])

