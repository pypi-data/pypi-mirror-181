import skfem
import numpy as np
import io


MESH_TYPE_MAPPING = {
    skfem.MeshTet1: 4,
    skfem.MeshHex1: 5,
#    skfem.MeshWedge1: 6,
    skfem.MeshTri1: 2,
    skfem.MeshQuad1: 3,
    skfem.MeshLine1: 1,
}


BOUNDARY_TYPE_MAPPING = {
    4: 2,
    2: 1,
    3: 1,
    5: 3,
}


template = """solution

MFEM mesh v1.0

dimension
{}

elements
{}
{}

boundary
{}
{}

vertices
{}
{}
{}

FiniteElementSpace
FiniteElementCollection: Linear
VDim: 2
Ordering: 0

0
1
2
3

"""

# POINT       = 0
# SEGMENT     = 1
# TRIANGLE    = 2
# SQUARE      = 3
# TETRAHEDRON = 4
# CUBE        = 5
# PRISM       = 6


def _to_int_string(arr):
    s = io.BytesIO()
    np.savetxt(s, arr, delimiter=' ', fmt='%d')
    return s.getvalue().decode()


def _to_float_string(arr):
    s = io.BytesIO()
    np.savetxt(s, arr, delimiter=' ')
    return s.getvalue().decode()


def to_mfem(m):
    bfacets = m.boundary_facets()
    nbfacets = len(bfacets)
    return template.format(
        m.dim(),
        m.nelements,
        _to_int_string(np.hstack((
            np.ones(m.nelements, dtype=np.int64)[:, None],
            (np.zeros(m.nelements, dtype=np.int64)[:, None]
             + MESH_TYPE_MAPPING[type(m)]),
            m.t.T,
        ))),
        nbfacets,
        _to_int_string(np.hstack((
            np.ones(nbfacets, dtype=np.int64)[:, None],
            (np.zeros(nbfacets, dtype=np.int64)[:, None]
             + BOUNDARY_TYPE_MAPPING[MESH_TYPE_MAPPING[type(m)]]),
            m.facets[:, bfacets].T,
        ))),        
        m.nvertices,
        m.doflocs.shape[0],
        _to_float_string(m.doflocs.T),
    )

