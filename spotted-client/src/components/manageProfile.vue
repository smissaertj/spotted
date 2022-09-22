<template>
  <div class="flex flex-col w-full px-64">
    <div
      class="card flex flex-shrink-0 shadow-2xl bg-base-100 glass rounded-box place-items-center"
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
  </div>
</template>

<script>
import { mapStores, mapActions } from "pinia";
import useUserStore from "@/stores/user";
export default {
  name: "manageProfile",
  data() {
    return {
      updateSchema: {
        password: "min:6",
        confirmPassword: "confirmed:@password",
      },
      update_in_submission: false,
      update_show_alert: false,
      update_alert_variant: "alert-success",
      update_alert_msg: "Updating profile...",
    };
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    ...mapActions(useUserStore, ["update", "checkUsername"]),
    async usernameAvailable(event) {
      if (event.target.value) {
        this.update_show_alert = false;
        const usernameAvailable = await this.checkUsername(event.target.value);
        if (!usernameAvailable) {
          this.update_show_alert = true;
          this.update_alert_variant = "alert-error";
          this.update_alert_msg = "Username is taken.";
          this.update_in_submission = true;
        } else {
          this.update_show_alert = false;
          this.update_in_submission = false;
        }
      }
    },
    async updateProfile(values) {
      this.update_in_submission = true;
      this.update_show_alert = true;
      this.update_alert_variant = "alert-warning";
      this.update_alert_msg = "Updating profile";
      try {
        await this.update(values);
        this.update_in_submission = false;
        this.update_show_alert = true;
        this.update_alert_variant = "alert-success";
        this.update_alert_msg = "Profile updated.";
        // TODO - Set Timeout then update_show_alert = false
      } catch (error) {
        console.log(error);
        this.update_in_submission = false;
        this.update_show_alert = true;
        this.update_alert_variant = "alert-error";
        this.update_alert_msg = error;
        return;
      }
    },
  },
};
</script>

<style scoped></style>
