<template>
  <div>
    <h2>{{$t('settings.title')}}</h2>

    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-if="uiLoaded">
      <div
        v-show="status.runningMaster > 0 || status.runningSlave > 0"
        class="alert alert-warning"
      >
        <button type="button" class="close">
          <div class="spinner"></div>
        </button>
        <span class="pficon pficon-warning-triangle-o"></span>
        <strong>{{$t('settings.task_in_progress')}}:</strong>
        {{status.runningMaster > 0 ?
        $t('settings.master_sync_with_slave') : status.runningSlave > 0 ? $t('settings.slave_sync_with_master') : ''}}.
      </div>
      <form class="form-horizontal" v-on:submit.prevent="saveConfig()">
        <div class="row">
          <div class="col-lg-12">
            <div class="col-md-6">
              <div class="form-group">
                <label class="col-sm-5 control-label">
                  {{$t('settings.status')}}
                </label>
                <div class="col-sm-5">
                  <input
                    v-model="configuration.status"
                    type="checkbox"
                    class="form-control"
                    true-value="enabled"
                    false-value="disabled"
                  >
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-5 control-label">
                  {{$t('settings.role')}}
                </label>
                <div :class="['col-sm-5', errors.role.hasError ? 'has-error' : '']">
                  <select
                    class="combobox form-control"
                    required
                    v-model="configuration.role"
                  >
                    <option value="null">{{$t('settings.role_null')}}</option>
                    <option value="master">{{$t('settings.role_master')}}</option>
                    <option value="slave">{{$t('settings.role_slave')}}</option>
                  </select>
                  <span v-if="errors.role.hasError" class="help-block">{{$t('settings.not_valid_role_selected')}}</span>
                </div>
              </div>
              
              <div v-if="configuration.role == 'master'">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.rsyncd_password')}}
                  </label>
                  <div class="col-sm-5">
                    <input
                      tabindex="0"
                      class="form-control"
                      :type="configuration.togglePass ? 'text' : 'password'"
                      v-model="configuration.rsyncdPassword"
                      required
                    >
                  </div>
                  <div class="col-sm-2">
                    <button
                      tabindex="-1"
                      @click="togglePass()"
                      type="button"
                      class="btn btn-primary adjust-top-min"
                    >
                      <span :class="[!configuration.togglePass ? 'fa fa-eye' : 'fa fa-eye-slash']"></span>
                    </button>
                  </div>
                </div>
                <div :class="['form-group', errors.slaveIp.hasError ? 'has-error' : '']">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.slave_ip')}}
                  </label>
                  <div class="col-sm-5">
                    <input
                      type="text"
                      class="form-control"
                      v-model="configuration.slaveIp"
                      required
                    >
                    <span v-if="errors.slaveIp.hasError" class="help-block">{{$t('settings.not_valid_ip_address')}}</span>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.sync_databases')}}
                  </label>
                  <div class="col-sm-5">
                    <input
                      v-model="configuration.databases"
                      type="checkbox"
                      class="form-control"
                      true-value="enabled"
                      false-value="disabled"
                    >
                  </div>
                </div>
              </div>
              
              <div v-else-if="configuration.role == 'slave'">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.rsyncd_password')}}
                  </label>
                  <div class="col-sm-5">
                    <input
                      tabindex="0"
                      class="form-control"
                      :type="configuration.togglePass ? 'text' : 'password'"
                      v-model="configuration.rsyncdPassword"
                      required
                    >
                  </div>
                  <div class="col-sm-2">
                    <button
                      tabindex="-1"
                      @click="togglePass()"
                      type="button"
                      class="btn btn-primary adjust-top-min"
                    >
                      <span :class="[!configuration.togglePass ? 'fa fa-eye' : 'fa fa-eye-slash']"></span>
                    </button>
                  </div>
                </div>
                <div :class="['form-group', errors.masterIp.hasError ? 'has-error' : '']">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.master_ip')}}
                  </label>
                  <div class="col-sm-5">
                    <input
                      type="text"
                      class="form-control"
                      v-model="configuration.masterIp"
                      required
                    >
                    <span v-if="errors.masterIp.hasError" class="help-block">{{$t('settings.not_valid_ip_address')}}</span>
                  </div>
                </div>
              </div>
              
              <!-- save button -->
              <div class="form-group">
                <label class="col-sm-5 control-label">
                </label>
                <div class="col-sm-5">
                  <button 
                    class="btn btn-primary" 
                    type="submit"
                  >
                    {{$t('save')}}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>

      <h3>{{$t('settings.actions')}}</h3>
      <form class="form-horizontal">
        <div class="row">
          <div class="col-lg-12">
            <div class="col-md-6">
              <div v-if="configuration.role == 'master'" class="form-group">
                <label class="col-sm-5 control-label">
                  {{$t('settings.hotsync_with_slave')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('settings.hotsync_with_slave')"
                    :chapter="'HotSyncWithSlave'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-5">
                  <button 
                    :disabled="status.runningMaster || configuration.status != 'enabled'"
                    class="btn btn-primary" 
                    type="button"
                    @click="hotsync('')"
                  >
                    {{$t('settings.hotsync')}}
                  </button>
                </div>
              </div>
              <div v-else-if="configuration.role == 'slave'">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.hotsync_from_master')}}
                    <doc-info
                      :placement="'top'"
                      :title="$t('settings.hotsync_from_master')"
                      :chapter="'HotSyncFromMaster'"
                      :inline="true"
                    ></doc-info>
                  </label>
                  <div class="col-sm-5">
                    <button 
                      :disabled="status.runningSlave || configuration.status != 'enabled'"
                      class="btn btn-primary" 
                      type="button"
                      @click="hotsync('-slave')"
                    >
                      {{$t('settings.hotsync_slave')}}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
        
  </div>
</template>

<script>
export default {
  name: "Settings",
  components: {
  },
  props: {
  },
  mounted() {
    this.getConfig();
    this.getHotsyncStatus();
    this.pollingStatus();
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      configuration: {
        status: null,
        role: null,
        masterIp: null,
        slaveIp: null,
        databases: null,
        rsyncdPassword: null,
        togglePass: false
      },
      status: {
        runningMaster: false,
        runningSlave: false
      },
      loaders: false,
      errors: this.initErrors()
    }
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage;
    },
    closeErrorMessage() {
      this.errorMessage = null;
    },
    getConfig() {
      var context = this;
      context.uiLoaded = false;
      nethserver.exec(
        ["nethserver-hotsync/settings/read"],
        { action: "configuration" },
        null,
        function(success) {
          try {
            context.configuration = JSON.parse(success).configuration;
            if (context.configuration.role.trim() == "") {
              context.configuration.role = "null";
            }
          } catch (e) {
            console.error(e);
          }
          context.uiLoaded = true;
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_reading_hotsync_configuration"), error);
        }
      );
    },
    getHotsyncStatus() {
      var context = this;
      nethserver.exec(
        ["nethserver-hotsync/settings/read"],
        { action: "hotsync-status" },
        null,
        function(success) {
          try {
            context.status = JSON.parse(success).status;
          } catch (e) {
            console.error(e);
          }
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_reading_hotsync_status"), error);
        }
      );
    },
    saveConfig() {
      var context = this;
      var settingsObj = {
        action: "edit",
        "configuration": {
          status: context.configuration.status,
          role: context.configuration.role,
          masterIp: context.configuration.masterIp,
          slaveIp: context.configuration.slaveIp,
          databases: context.configuration.databases,
          rsyncdPassword: context.configuration.rsyncdPassword
        }
      };
      context.loaders = true;
      context.errors = context.initErrors();
      nethserver.exec(
        ["nethserver-hotsync/settings/validate"],
        settingsObj,
        null,
        function(success) {
          context.loaders = false;
          
          nethserver.notifications.success = context.$i18n.t(
            "settings.settings_updated_ok"
          );
          
          nethserver.notifications.error = context.$i18n.t(
            "settings.settings_updated_error"
          );
              
          // update values
          nethserver.exec(
            ["nethserver-hotsync/settings/update"],
            settingsObj,
            function(stream) {
              console.info("nethserver-hotsync-save", stream);
            },
            function(success) {
              context.getConfig();
            },
            function(error, data) {
              console.error(error, data);
            },
            true //sudo
          );
        },
        function(error, data) {
          var errorData = {};
          context.loaders = false;
          context.errors = context.initErrors();
          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.errors[attr.parameter].hasError = true;
              context.errors[attr.parameter].message = attr.error;
            }
          } catch (e) {
            console.error(e);
          }
        },
        true // sudo
      );
    },
    initErrors() {
      return {
        slaveIp: {
          hasError: false,
          message: ""
        },
        masterIp: {
          hasError: false,
          message: ""
        },
        role: {
          hasError: false,
          message: ""
        }
      }
    },
    hotsync(type) {
      var context = this;
      nethserver.exec(
        ["nethserver-hotsync/settings/execute"],
        { action: "hotsync" + type },
        function(stream) {
          console.info("hotsync" + type, stream);
        },
        function(success) {
          nethserver.notifications.success = context.$i18n.t(
            "settings.success_hotsync_command"
          );
          context.getHotsyncStatus();
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_hotsync_command"), error);
        }
      );
    },
    pollingStatus() {
      var context = this;
      context.pollingIntervalId = setInterval(function() {
        context.getHotsyncStatus();
      }, 2500);
    },
    togglePass() {
      this.configuration.togglePass = !this.configuration.togglePass;
    }
  }
};
</script>

<style scoped>
</style>
