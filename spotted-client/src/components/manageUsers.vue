<template>
  <div class="toast toast-top toast-end mt-20" v-if="toast_show">
    <div class="alert" :class="toast_variant">
      <div>
        <font-awesome-icon icon="fa-solid fa-circle-info" class="my-2" />
        <span>{{ toast_msg }}</span>
      </div>
    </div>
  </div>
  <div class="m-auto" v-if="!this.users">
    <font-awesome-icon
      icon="fa-solid fa-spinner"
      class="fa-spin text-accent"
      size="3x"
    />
  </div>
  <div
    class="alert alert-error shadow-lg m-auto w-1/2"
    v-else-if="users_show_alert"
  >
    <div>
      <span>{{ users_alert_msg }}</span>
    </div>
  </div>
  <div class="overflow-y-auto w-full" v-else>
    <table class="table min-w-full m-auto text-center">
      <!-- head -->
      <thead>
        <tr class="bg-accent">
          <th class="w-1/12 bg-accent-content/25 text-secondary-content">
            <label> Select </label>
          </th>
          <th class="w-1/12 bg-accent-content/25 text-secondary-content">
            User
          </th>
          <th class="w-1/12 bg-accent-content/25 text-secondary-content">
            Status
          </th>
          <th class="w-1/12 bg-accent-content/25 text-secondary-content">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <!-- row 1 -->
        <tr v-for="user in users" :key="user.uid">
          <th>
            <label>
              <input type="checkbox" class="checkbox" v-model="user.selected" />
            </label>
          </th>
          <td>
            <div class="flex flex-row justify-center">
              <div>
                <div class="font-bold">{{ user.displayName }}</div>
                <div class="text-sm opacity-50">{{ user.email }}</div>
              </div>
            </div>
          </td>
          <td
            :class="{
              'text-success': !user.isDisabled,
              'text-error': user.isDisabled,
            }"
          >
            {{ user.isDisabled ? "Disabled" : "Active" }}
            <div class="text-sm opacity-50 text-primary">
              {{ user.isAdmin ? "Administrator" : "" }}
            </div>
          </td>
          <td>
            <button
              class="btn btn-ghost btn-xs hover:btn-error"
              :disabled="!user.selected"
              @click.prevent="changeAccountState(user.uid, 'delete')"
            >
              Delete
            </button>
            <button
              class="btn btn-ghost btn-xs mx-2"
              :disabled="!user.selected"
              :class="{
                'hover:btn-success': user.isDisabled,
                'hover:btn-warning': !user.isDisabled,
              }"
              @click.prevent="
                changeAccountState(
                  user.uid,
                  user.isDisabled ? 'enable' : 'disable'
                )
              "
            >
              {{ user.isDisabled ? "Activate" : "Deactivate" }}
            </button>
          </td>
        </tr>
      </tbody>
      <!-- foot -->
      <tfoot>
        <tr class="bg-accent">
          <th class="bg-accent-content/25 text-secondary-content">Select</th>
          <th class="bg-accent-content/25 text-secondary-content">User</th>
          <th class="bg-accent-content/25 text-secondary-content">Status</th>
          <th class="bg-accent-content/25 text-secondary-content">Actions</th>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script>
import { mapStores } from "pinia";
import useUserStore from "@/stores/user";
import axios from "axios";
const authService = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
export default {
  name: "manageUsers",
  data() {
    return {
      users: "",
      users_show_alert: false,
      users_alert_msg: "Something went wrong.",
      toast_show: false,
      toast_variant: "alert-success",
      toast_msg: "Success!",
    };
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    async getAllUsers() {
      try {
        const result = await authService.post("/users/list", {
          id_token: this.userStore.idToken,
        });
        this.users = result.data;
      } catch (error) {
        console.log(error);
        this.users_show_alert = true;
        this.users_alert_msg = error.data;
      }
    },
    async changeAccountState(uid, action) {
      try {
        this.toast_show = true;
        this.toast_variant = "alert-warning";
        this.toast_msg = "Updating User Record";
        const result = await authService.post("/user/state/" + action, {
          uid: uid,
          id_token: this.userStore.idToken,
        });
        this.toast_variant = "alert-success";
        this.toast_msg = result.data.message;
        setTimeout(() => {
          this.toast_show = false;
        }, 3000);
        this.getAllUsers();
      } catch (error) {
        console.log(error);
        this.toast_show = true;
        this.toast_variant = "alert-error";
        this.toast_msg = error.data.message;
        setTimeout(() => {
          this.toast_show = false;
        }, 3000);
      }
    },
  },
  beforeMount() {
    this.getAllUsers();
  },
};
</script>

<style scoped></style>
