/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

class GymDashboard extends Component {
    static template = "gym_management.GymDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            total_members: 0,
            active_members: 0,
            expired_members: 0,
            inactive_members: 0,
            total_trainers: 0,
            active_memberships: 0,
            workout_plans: 0,
            diet_plans: 0,
            loading: true,
        });
        onWillStart(this.loadData.bind(this));
    }

    async loadData() {
        const [
            totalMembers,
            activeMembers,
            expiredMembers,
            inactiveMembers,
            totalTrainers,
            activeMemberships,
            workoutPlans,
            dietPlans,
        ] = await Promise.all([
            this.orm.searchCount("gym.member", []),
            this.orm.searchCount("gym.member", [["membership_status", "=", "active"]]),
            this.orm.searchCount("gym.member", [["membership_status", "=", "expired"]]),
            this.orm.searchCount("gym.member", [["membership_status", "=", "inactive"]]),
            this.orm.searchCount("gym.trainer", []),
            this.orm.searchCount("gym.membership", [["state", "=", "active"]]),
            this.orm.searchCount("gym.workout.plan", []),
            this.orm.searchCount("gym.diet.plan", []),
        ]);

        this.state.total_members = totalMembers;
        this.state.active_members = activeMembers;
        this.state.expired_members = expiredMembers;
        this.state.inactive_members = inactiveMembers;
        this.state.total_trainers = totalTrainers;
        this.state.active_memberships = activeMemberships;
        this.state.workout_plans = workoutPlans;
        this.state.diet_plans = dietPlans;
        this.state.loading = false;
    }

    openMembers(status) {
        const domain = status ? [["membership_status", "=", status]] : [];
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Members",
            res_model: "gym.member",
            view_mode: "list,kanban,form",
            domain: domain,
            context: {},
        });
    }

    openTrainers() {
        this.action.doAction("gym_management.action_gym_trainer");
    }

    openMemberships(state) {
        const domain = state ? [["state", "=", state]] : [];
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Memberships",
            res_model: "gym.membership",
            view_mode: "list,form",
            domain: domain,
        });
    }

    openWorkoutPlans() {
        this.action.doAction("gym_management.action_gym_workout_plan");
    }

    openDietPlans() {
        this.action.doAction("gym_management.action_gym_diet_plan");
    }
}

registry.category("actions").add("gym_dashboard", GymDashboard);
