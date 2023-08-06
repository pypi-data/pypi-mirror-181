import cffi, os, sys
import numpy
import numpy as np


def load_lib():

    HERE = os.path.dirname(__file__)
    if sys.platform.startswith('linux'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "lib", "libsextbal.so"))
    elif sys.platform.startswith('win32'):
        LIB_FILE_NAME = os.path.abspath(os.path.join(HERE, ".", "compiled", "build", "bin", "libsextbal.dll"))
    else:
        raise Exception('Неподдерживаемая платформа')
    ffi = cffi.FFI()

    header_file = os.path.abspath(os.path.join(HERE, '.', 'compiled', 'kontur', 'csv_header.txt'))

    with open(header_file, encoding='utf8') as header_fp:
        header = ffi.cdef(header_fp.read())

    lib = ffi.dlopen(LIB_FILE_NAME)

    return ffi, lib

FFI, KONTUR_LIB = load_lib()

class KonturSolver:

    name = 'kontur_solver'

    preprocessed_data = dict(
        ng=None,
        nh=None,
        nk=None,
        nfl=None,
        d=None,
        hb=None,
        xct=None,
        yint=None,
        geometry_data=None
    )

    def run(self, data, global_state):
        p_data = self.preprocessed_data
        solver = KONTUR_LIB.CSV_New()
        KONTUR_LIB.CSV_SetNG(solver, p_data['ng'])
        KONTUR_LIB.CSV_SetNH(solver, p_data['nh'])
        KONTUR_LIB.CSV_SetNK(solver, p_data['nk'])
        KONTUR_LIB.CSV_SetNFL(solver, p_data['nfl'])
        KONTUR_LIB.CSV_SetDia(solver, p_data['d'])
        KONTUR_LIB.CSV_SetHb(solver, p_data['hb'])
        KONTUR_LIB.CSV_SetXct(solver, p_data['xct'])
        KONTUR_LIB.CSV_SetYInt(solver, p_data['yint'])

        for i, primitive in enumerate(p_data['geometry_data']):
            KONTUR_LIB.CSV_AddGeom(solver, i, primitive['type'], primitive['x1'], primitive['x2'],
                                   primitive['r1'], primitive['r2'], primitive['R'], primitive['n'])

        settings = data['settings']['kontur']

        attack_angle = np.linspace(settings['alpha_0'], settings['alpha_n'], settings['n_alpha'])
        mach_list = np.linspace(settings['mach_0'], settings['mach_n'], settings['n_mach'])

        mesh_tren = np.empty((attack_angle.shape[0], mach_list.shape[0]))
        mesh_don = np.empty_like(mesh_tren)
        mesh_voln = np.empty_like(mesh_tren)
        mesh_pois = np.empty_like(mesh_tren)
        mesh_cn = np.empty_like(mesh_tren)
        mesh_cy = np.empty_like(mesh_tren)
        mesh_xcd = np.empty_like(mesh_tren)
        mesh_cx = np.empty_like(mesh_tren)
        mesh_cyal = np.empty_like(mesh_tren)
        mesh_cmal = np.empty_like(mesh_tren)
        mesh_mxwx = np.empty_like(mesh_tren)
        mesh_mzwz = np.empty_like(mesh_tren)

        for i, atk_angl in enumerate(attack_angle):
            for j, mach in enumerate(mach_list):
                KONTUR_LIB.CSV_Solve(solver, mach, atk_angl)
                mesh_tren[i, j] = KONTUR_LIB.CSV_GetTren(solver)
                mesh_don[i, j] = KONTUR_LIB.CSV_GetDon(solver)
                mesh_voln[i, j] = KONTUR_LIB.CSV_GetVoln(solver)
                mesh_pois[i, j] = KONTUR_LIB.CSV_GetPois(solver)
                mesh_cn[i, j] = KONTUR_LIB.CSV_GetCn(solver)
                mesh_cy[i, j] = KONTUR_LIB.CSV_GetCy(solver)
                mesh_xcd[i, j] = KONTUR_LIB.CSV_GetXcd(solver)
                mesh_cx[i, j] = KONTUR_LIB.CSV_GetCx(solver)
                mesh_cyal[i, j] = KONTUR_LIB.CSV_GetCyAl(solver)
                mesh_cmal[i, j] = KONTUR_LIB.CSV_GetCmAl(solver)
                mesh_mxwx[i, j] = KONTUR_LIB.CSV_GetMxWx(solver)
                mesh_mzwz[i, j] = KONTUR_LIB.CSV_GetMzWz(solver)

        global_state[KonturSolver.name] = dict(
            mesh_tren=mesh_tren,
            mesh_don=mesh_don,
            mesh_voln=mesh_voln,
            mesh_pois=mesh_pois,
            mesh_cn=mesh_cn,
            mesh_cy=mesh_cy,
            mesh_xcd=mesh_xcd,
            mesh_cx=mesh_cx,
            mesh_cyal=mesh_cyal,
            mesh_cmal=mesh_cmal,
            mesh_mxwx=mesh_mxwx,
            mesh_mzwz=mesh_mzwz
        )


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def print_solver(solver):
        print(
            KONTUR_LIB.CSV_GetMach(solver),
            KONTUR_LIB.CSV_GetTren(solver),
            KONTUR_LIB.CSV_GetDon(solver),
            KONTUR_LIB.CSV_GetVoln(solver),
            KONTUR_LIB.CSV_GetPois(solver),
            KONTUR_LIB.CSV_GetCn(solver),
            KONTUR_LIB.CSV_GetCy(solver),
            KONTUR_LIB.CSV_GetXcd(solver),
            KONTUR_LIB.CSV_GetCx(solver),
            KONTUR_LIB.CSV_GetCyAl(solver),
            KONTUR_LIB.CSV_GetCmAl(solver),
            KONTUR_LIB.CSV_GetMxWx(solver),
            KONTUR_LIB.CSV_GetMzWz(solver),
        )

    def test_kontur():
        solver = KONTUR_LIB.CSV_New()
        KONTUR_LIB.CSV_SetNG(solver, 4)
        KONTUR_LIB.CSV_SetNH(solver, 5)
        KONTUR_LIB.CSV_SetNK(solver, 7)
        KONTUR_LIB.CSV_SetNFL(solver, 2)
        KONTUR_LIB.CSV_SetDia(solver, 0.1524)
        KONTUR_LIB.CSV_SetHb(solver, 0.01 * 0.1524)
        KONTUR_LIB.CSV_SetXct(solver, 0.533)
        KONTUR_LIB.CSV_SetYInt(solver, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 0, KONTUR_LIB.G_CYLINDR, 0., .01, .01, .01, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 1, KONTUR_LIB.G_CONE, .01, .06, .01, .02, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 2, KONTUR_LIB.G_CONE, .06, .18, .02, .0425, 0., 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 3, KONTUR_LIB.G_OGIVE, .18, .457, .0425, .0762, 3.22, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 4, KONTUR_LIB.G_CYLINDR, .457, .712, .0762, .0762, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 5, KONTUR_LIB.G_CONE, .712, .723, .0762, .0748, .0, 0.)
        KONTUR_LIB.CSV_AddGeom(solver, 6, KONTUR_LIB.G_CONE, .723, .863, .0748, .06675, .0, 0.)

        attack_angle = np.linspace(0., 2., 5)
        mach_list = np.linspace(0.4, 3.1)

        mesh_tren = np.empty((attack_angle.shape[0], mach_list.shape[0]))
        mesh_don = np.empty_like(mesh_tren)
        mesh_voln = np.empty_like(mesh_tren)
        mesh_pois = np.empty_like(mesh_tren)
        mesh_cn = np.empty_like(mesh_tren)
        mesh_cy = np.empty_like(mesh_tren)
        mesh_xcd = np.empty_like(mesh_tren)
        mesh_cx = np.empty_like(mesh_tren)
        mesh_cyal = np.empty_like(mesh_tren)
        mesh_cmal = np.empty_like(mesh_tren)
        mesh_mxwx = np.empty_like(mesh_tren)
        mesh_mzwz = np.empty_like(mesh_tren)

        for i, atk_angl in enumerate(attack_angle):
            # print(f'Угол нутации: {atk_angl}')
            for j, mach in enumerate(mach_list):
                KONTUR_LIB.CSV_Solve(solver, mach, atk_angl)
                # KONTUR_LIB.CSV_GetMach(solver)
                mesh_tren[i, j] = KONTUR_LIB.CSV_GetTren(solver)
                mesh_don[i, j] = KONTUR_LIB.CSV_GetDon(solver)
                mesh_voln[i, j] = KONTUR_LIB.CSV_GetVoln(solver)
                mesh_pois[i, j] = KONTUR_LIB.CSV_GetPois(solver)
                mesh_cn[i, j] = KONTUR_LIB.CSV_GetCn(solver)
                mesh_cy[i, j] = KONTUR_LIB.CSV_GetCy(solver)
                mesh_xcd[i, j] = KONTUR_LIB.CSV_GetXcd(solver)
                mesh_cx[i, j] = KONTUR_LIB.CSV_GetCx(solver)
                mesh_cyal[i, j] = KONTUR_LIB.CSV_GetCyAl(solver)
                mesh_cmal[i, j] = KONTUR_LIB.CSV_GetCmAl(solver)
                mesh_mxwx[i, j] = KONTUR_LIB.CSV_GetMxWx(solver)
                mesh_mzwz[i, j] = KONTUR_LIB.CSV_GetMzWz(solver)

        plt.plot(mach_list, mesh_cx[0], label='alpha 0.')
        plt.plot(mach_list, mesh_cx[1], label='alpha 1.')
        plt.plot(mach_list, mesh_cx[2], label='alpha 1.5')
        plt.plot(mach_list, mesh_cx[3], label='alpha 2.')
        plt.legend()
        plt.show()

    test_kontur()
