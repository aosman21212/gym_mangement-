# -*- coding: utf-8 -*-


def post_init_hook(env):
    """Assign Odoo admin users to the Gym Administrator group after installation."""
    gym_admin_group = env.ref('gym_management.group_gym_admin', raise_if_not_found=False)
    if not gym_admin_group:
        return
    admin_users = env['res.users'].search([
        ('groups_id', 'in', [env.ref('base.group_system').id]),
        ('groups_id', 'not in', [gym_admin_group.id]),
    ])
    if admin_users:
        env.cr.execute(
            "INSERT INTO res_groups_users_rel (gid, uid) "
            "SELECT %s, uid FROM unnest(%s::int[]) AS uid "
            "ON CONFLICT DO NOTHING",
            (gym_admin_group.id, admin_users.ids),
        )
