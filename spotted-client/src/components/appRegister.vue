<template>
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <div class="card-body bg-base-300">
      <vee-form
        class="form-control"
        :validation-schema="registerSchema"
        @submit="createAccount"
      >
        <div class="form-control">
          <vee-field
            type="text"
            placeholder="Username"
            class="input input-bordered"
            name="username"
            @focusout.prevent="usernameAvailable($event)"
            required
          />
          <ErrorMessage class="text-red-600" name="username" />
        </div>
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
          <vee-field
            type="password"
            placeholder="Confirm Password"
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
            :disabled="register_in_submission"
          >
            Register
          </button>
          <div
            class="alert shadow-lg mt-2 justify-center font-bold"
            :class="register_alert_variant"
            v-if="register_show_alert"
          >
            <div>
              <span>{{ register_alert_msg }}</span>
            </div>
          </div>
        </div>
      </vee-form>
      <div class="divider">OR</div>
      <a href="/app">
        <button class="btn btn-primary btn-block">Start Exploring</button>
      </a>
    </div>
  </div>
</template>

<script>
import { mapActions } from "pinia";
import useUserStore from "@/stores/user";

export default {
  name: "appRegister",
  data() {
    return {
      registerSchema: {
        username: "required",
        email: "required|email",
        password: "required|min:6",
        confirmPassword: "required|confirmed:@password",
      },
      register_in_submission: false,
      register_show_alert: false,
      register_alert_variant: "alert-success",
      register_alert_msg: "Creating account...",
    };
  },
  methods: {
    ...mapActions(useUserStore, {
      createUser: "register",
      checkUsername: "checkUsername",
    }),
    async createAccount(values) {
      this.register_in_submission = true;
      this.register_show_alert = true;
      this.register_alert_variant = "alert-warning";
      this.register_alert_msg = "Creating account...";
      try {
        await this.createUser(values);
        //TODO Set Time out before redirect
        this.$router.push("/manage");
      } catch (error) {
        this.register_in_submission = false;
        this.register_show_alert = true;
        this.register_alert_variant = "alert-error";
        this.register_alert_msg = error.message;
        return;
      }
      this.register_show_alert = true;
      this.register_alert_variant = "alert-success";
      this.register_alert_msg = "Success! Account created.";
    },
    async usernameAvailable(event) {
      if (event.target.value) {
        const usernameAvailable = await this.checkUsername(event.target.value);
        if (!usernameAvailable) {
          this.register_show_alert = true;
          this.register_alert_variant = "alert-error";
          this.register_alert_msg = "Username is taken.";
          this.register_in_submission = true;
        } else {
          this.register_show_alert = false;
          this.register_in_submission = false;
        }
      }
    },
  },
};
</script>
