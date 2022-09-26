<template>
  <app-google-map />
  <div
    class="card flex shadow-2xl bg-base-100 rounded glass place-items-center w-full h-1/2"
  >
    <div class="card-body">
      <vee-form
        class="form-control"
        :validation-schema="updateSchema"
        @submit="updateProfile"
      >
        <div class="form-control">
          <label class="input-group">
            <span class="label-text">Username</span>

            <vee-field
              type="text"
              placeholder=""
              class="input input-bordered w-full"
              name="username"
              v-model="userStore.displayName"
              @focusout.prevent="usernameAvailable($event)"
              required
            />
          </label>
          <ErrorMessage class="text-red-600" name="username" />
        </div>
        <div class="form-control mt-2">
          <label class="input-group">
            <span class="label-text">Email</span>
            <vee-field
              type="email"
              placeholder=""
              class="input input-bordered w-full"
              name="email"
              v-model="userStore.email"
              required
            />
          </label>
          <ErrorMessage class="text-red-600" name="email" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="password"
            placeholder="New Password"
            class="input input-bordered w-full"
            name="password"
            required
          />
          <ErrorMessage class="text-red-600" name="password" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="password"
            placeholder="Confirm New Password"
            class="input input-bordered"
            name="confirmPassword"
            required
          />
          <ErrorMessage class="text-red-600" name="confirmPassword" />
        </div>

        <div class="form-control mt-2">
          <button
            class="btn btn-primary"
            type="submit"
            :disabled="update_in_submission"
          >
            Update
          </button>
          <div
            class="alert shadow-lg mt-2 justify-center font-bold"
            :class="update_alert_variant"
            v-if="update_show_alert"
          >
            <div>
              <span
                ><font-awesome-icon
                  icon="fa-solid fa-spinner"
                  class="fa-spin mr-2"
                  v-if="update_alert_variant == 'alert-warning'"
                />{{ update_alert_msg }}</span
              >
            </div>
          </div>
        </div>
      </vee-form>
    </div>
  </div>
</template>

<script>
import { mapStores, mapActions } from "pinia";
import useUserStore from "@/stores/user";
import appGoogleMap from "@/components/appGoogleMap.vue";
export default {
  name: "newSubmission",
  components: {
    appGoogleMap,
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    ...mapActions(useUserStore, ["update", "checkUsername"]),
  },
};
</script>

<style scoped></style>
