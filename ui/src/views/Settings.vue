<template>
  <div>
    <h1>{{$t('settings.title')}}</h1>

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
        v-show="configuration.runningMaster > 0 || configuration.runningSlave > 0 || configuration.runningPromote > 0"
        class="alert alert-warning"
      >
        <button type="button" class="close">
          <div class="spinner"></div>
        </button>
        <span class="pficon pficon-warning-triangle-o"></span>
        <strong>{{$t('settings.task_in_progress')}}:</strong>
        {{configuration.runningMaster > 0 ?
        $t('settings.master_sync_with_slave') : configuration.runningSlave > 0 ? $t('settings.slave_sync_with_master') : configuration.runningPromote > 0 ? $t('settings.promote_is_running') : ''}}.
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
                      type="text"
                      class="form-control"
                      v-model="configuration.rsyncdPassword"
                      required
                    >
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
                      type="text"
                      class="form-control"
                      v-model="configuration.rsyncdPassword"
                      required
                    >
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
                </label>
                <div class="col-sm-5">
                  <button 
                    :disabled="configuration.runningMaster || configuration.status != 'enabled'"
                    class="btn btn-primary" 
                    type="button"
                    @click="hotsync()"
                  >
                    {{$t('settings.hotsync')}}
                  </button>
                </div>
              </div>
              <div v-else-if="configuration.role == 'slave'">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.hotsync_from_master')}}
                  </label>
                  <div class="col-sm-5">
                    <button 
                      :disabled="configuration.runningSlave || configuration.runningPromote || configuration.status != 'enabled'"
                      class="btn btn-primary" 
                      type="button"
                      @click="hotsync('-slave')"
                    >
                      {{$t('settings.hotsync_slave')}}
                    </button>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('settings.promote')}}
                  </label>
                  <div class="col-sm-5">
                    <button 
                      :disabled="configuration.runningPromote || configuration.runningSlave || configuration.status != 'enabled'"
                      class="btn btn-danger" 
                      type="button"
                      @click="openPromote()"
                    >
                      {{$t('settings.promote_btn')}}
                    </button>
                  </div>
                </div>  
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
    
    <div class="modal" id="promoteModal" tabindex="-1" role="dialog" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">
              {{$t('settings.start_promote_task')}}
            </h4>
          </div>
          <form
            class="form-horizontal"
            v-on:submit.prevent="promote()"
          >
            <div class="modal-body">
              <div class="form-group">
                <label
                  class="col-sm-3 control-label"
                  for="textInput-modal-markup"
                >{{$t('are_you_sure')}}?</label>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
              <button class="btn btn-danger" type="submit">{{$t('settings.promote')}}</button>
            </div>
          </form>
        </div>
      </div>
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
        runningMaster: false,
        runningSlave: false,
        runningPromote: false
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
    getConfig(type) {
      var context = this;
      if (type != "update") {
        context.uiLoaded = false;
      }
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
          if (type != "update") {
            context.uiLoaded = true;
          }
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_reading_hotsync_configuration"), error);
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

          // update values
          nethserver.exec(
            ["nethserver-hotsync/settings/update"],
            settingsObj,
            function(stream) {
              console.info("nethserver-hotsync-save", stream);
            },
            function(success) {
              context.getConfig();
              nethserver.notifications.success = context.$i18n.t(
                "settings.settings_updated_ok"
              );
            },
            function(error, data) {
              console.error(error, data);
              nethserver.notifications.error = context.$i18n.t(
                "settings.settings_updated_error"
              );
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
          context.getConfig('update');
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_hotsync_command"), error);
        }
      );
    },
    promote() {
      var context = this;
      nethserver.exec(
        ["nethserver-hotsync/settings/execute"],
        { action: "promote" },
        function(stream) {
          console.info("promote", stream);
        },
        function(success) {
          nethserver.notifications.success = context.$i18n.t(
            "settings.success_promote_command"
          );
          context.getConfig('update');
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_promote_command"), error);
        }
      );
    },
    pollingStatus() {
      var context = this;
      context.pollingIntervalId = setInterval(function() {
        context.getConfig('update');
      }, 2500);
    },
    openPromote() {
      $('#promoteModal').modal('show');
    }
  }
};
</script>

<style scoped>
</style>