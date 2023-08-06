"""
individually configurable setup hook
====================================

by replacing the function call of :func:`~aedev.setup_project.project_env_vars` in the :mod:`aedev.setup_project` module
of a project with a call to the function :func:`hooked_project_env_vars`, provided by this module, an individual hook
will be executed automatically just before the execution of the :mod:`setuptools` :meth:`~setuptools.setup` method.

this setup hook can be used e.g. to adapt/extend the variables and constants of the project environment variable
mapping. also, the settings of a portion of a namespace project can be configured individually by adding a hook module
(containing a hook method) into the portions project working tree root folder. the default names of the hook module and
method are specified by the constant :data:`NAMESPACE_EXTEND_ENTRY_POINT`, which gets also added automatically into the
project environment variable mapping by the function :func:`hooked_project_env_vars` of this module.
"""
from ae.base import in_wd                                                   # type: ignore
from ae.inspector import module_attr, try_call                              # type: ignore
from aedev.setup_project import PevType, pev_str, project_env_vars          # type: ignore


__version__ = '0.3.5'


NAMESPACE_EXTEND_ENTRY_POINT = "setup_hooks:extend_project_env_vars"    #: module:method default names of the setup hook


def hooked_project_env_vars(project_path: str = "") -> PevType:
    """ called from setup.py instead of :func:`~aedev.setup_project.project_env_vars` to determine the project vars.

    :param project_path:        optional rel/abs path of package/app/project root (def=current working directory).
    :return:                    project environment variables mapping/dict, optionally updated by hook.
    """
    pev = project_env_vars(project_path=project_path, from_setup=True)
    if 'NAMESPACE_EXTEND_ENTRY_POINT' not in pev:
        pev['NAMESPACE_EXTEND_ENTRY_POINT'] = NAMESPACE_EXTEND_ENTRY_POINT

    # finally, check if optional hook exists and if yes then run it for to change the pev values accordingly
    with in_wd(project_path):
        pev_update_hook(pev)

    return pev


def pev_update_hook(pev: PevType) -> bool:
    """ check if optional NAMESPACE_EXTEND_ENTRY_POINT hook file exists and if yes then run it to change pev values.

    :param pev:                 namespace environment variables.
    :return:                    True if hook got called, else False.
    """
    entry_point = pev_str(pev, 'NAMESPACE_EXTEND_ENTRY_POINT')
    callee = module_attr(*entry_point.split(':'))
    if callee:
        try_call(callee, pev)
        if pev_str(pev, 'NAMESPACE_EXTEND_ENTRY_POINT') != entry_point:
            # run the redirected hook recursively, now with a new hook file or function name
            pev_update_hook(pev)
    return bool(callee)
