<template>
  <div class="drawer drawer-mobile border-t border-b">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col items-center justify-center">
      <manage-profile v-if="this.$route.name == 'profile'" />
      <manage-users v-else-if="this.$route.name == 'manageUsers'" />
      <div v-else>Page content here</div>
      <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden"
        >Menu</label
      >
    </div>
    <div class="drawer-side border-r">
      <label for="my-drawer-2" class="drawer-overlay"></label>
      <ul class="menu bg-base-100 w-56">
        <li>
          <router-link
            :to="{ name: 'newSubmission' }"
            exact-active-class="active"
            ><font-awesome-icon icon="fa-solid fa-circle-plus" />New
            Submission</router-link
          >
        </li>
        <li>
          <router-link
            :to="{ name: 'mySubmissions' }"
            exact-active-class="active"
            ><font-awesome-icon icon="fa-solid fa-rectangle-list" />My
            Submissions</router-link
          >
        </li>

        <li>
          <router-link :to="{ name: 'myComments' }" exact-active-class="active"
            ><font-awesome-icon icon="fa-solid fa-comments" />My
            Comments</router-link
          >
        </li>
        <li>
          <router-link :to="{ name: 'profile' }" exact-active-class="active"
            ><font-awesome-icon icon="fa-solid fa-user" />Profile</router-link
          >
        </li>

        <li v-if="userStore.userIsAdmin">
          <router-link :to="{ name: 'manageUsers' }" exact-active-class="active"
            ><font-awesome-icon icon="fa-solid fa-wrench" />Manage
            Users</router-link
          >
        </li>
        <li v-if="userStore.userIsAdmin">
          <a
            ><font-awesome-icon icon="fa-solid fa-wrench" />Manage
            Submissions</a
          >
        </li>
        <li v-if="userStore.userIsAdmin">
          <a><font-awesome-icon icon="fa-solid fa-wrench" />Manage Comments</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapStores } from "pinia";
import useUserStore from "@/stores/user.js";
import manageProfile from "@/components/manageProfile.vue";
import manageUsers from "@/components/manageUsers.vue";
export default {
  name: "appProfile",
  components: {
    manageProfile,
    manageUsers,
  },
  computed: {
    ...mapStores(useUserStore),
  },
};
</script>
