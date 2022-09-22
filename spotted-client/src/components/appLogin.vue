<template>
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-300 m-auto">
    <div class="card-body bg-base-300">
      <vee-form
        class="form-control"
        :validation-schema="loginSchema"
        @submit="login"
      >
        <div class="form-control mt-2">
          <vee-field
            type="email"
            placeholder="Email"
            class="input input-bordered"
            name="email"
            required
          />
          <ErrorMessage class="text-red-600" name="email" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="password"
            placeholder="Password"
            class="input input-bordered"
            name="password"
            required
          />
          <ErrorMessage class="text-red-600" name="password" />
        </div>
        <div class="form-control mt-2">
          <button
            class="btn btn-primary"
            type="submit"
            :disabled="login_in_submission"
          >
            Login
          </button>
        </div>
      </vee-form>
      <div class="form-control mt-2">
        <div
          class="alert shadow-lg mt-2 justify-center font-bold"
          v-if="login_show_alert"
          :class="login_alert_variant"
        >
          <div>
            <span>{{ login_alert_msg }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import useUserStore from "@/stores/user";
export default {
  name: "appLogin",
  data() {
    return {
      loginSchema: {
        email: "required|email",
        password: "required",
      },
      login_in_submission: false,
      login_show_alert: false,
      login_alert_variant: "alert-success",
      login_alert_msg: "Please wait! You're being logged in.",
    };
  },
  methods: {
    ...mapActions(useUserStore, ["authenticate"]),
    async login(values) {
      this.login_in_submission = true;
      this.login_show_alert = true;
      this.login_alert_variant = "alert-warning";
      this.login_alert_msg = "Please wait! We're logging you in.";
      try {
        await this.authenticate(values);
        this.login_alert_variant = "alert-success";
        this.login_alert_msg = "Success! You're now logged in.";
        //TODO - Set a timeout before redirecting the user
        this.$router.push({ name: "newSubmission" });
      } catch (error) {
        this.login_in_submission = false;
        this.login_alert_variant = "alert-error";
        this.login_alert_msg = "Invalid login details.";
        return;
      }
    },
  },
};
</script>

<style scoped></style>
