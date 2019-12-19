<template>
  <div>
    <h1>{{$t('dashboard.title')}}</h1>
      <!-- error message -->
      <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
        <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
          <span class="pficon pficon-close"></span>
        </button>
        <span class="pficon pficon-error-circle-o"></span>
        {{ errorMessage }}.
      </div>

      <div v-show="!uiLoaded" class="spinner spinner-lg"></div>
      <div v-show="uiLoaded">
        <h3>{{$t('dashboard.hotsync_configuration')}}</h3>
        <div class="row">
          <div class="col-lg-12">
            <div class="col-md-6">
              <form class="form-horizontal">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_status')}}
                  </label>
                  <div class="col-sm-5">
                    <span
                      :class="hotsync.status == 'enabled' ? 'pficon pficon-ok' : 'pficon-off'"
                      data-toggle="tooltip"
                      data-placement="top"
                      :title="$t('dashboard.status')+': '+ (hotsync.status == 'enabled' ? $t('dashboard.enabled') : $t('dashboard.disabled'))"
                    ></span>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_role')}}
                  </label>
                  <div class="col-sm-5">
                    {{hotsync.role}}
                  </div>
                </div>
              </form>
              <form v-if="hotsync.role == 'master'" class="form-horizontal">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_slave_host')}}
                  </label>
                  <div class="col-sm-5">
                    {{hotsync.slaveIp}}
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_slave_port')}}
                  </label>
                  <div class="col-sm-5">
                    {{hotsync.slavePort}}
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_sync_databases')}}
                  </label>
                  <div class="col-sm-5">
                    <span v-if="hotsync.databases == 'enabled'">{{$t('dashboard.enabled')}}</span>
                    <span v-else>{{$t('dashboard.disabled')}}</span>
                  </div>
                </div>
              </form>
              <form v-else-if="hotsync.role == 'slave'" class="form-horizontal">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.hotsync_master_host')}}
                  </label>
                  <div class="col-sm-5">
                    {{hotsync.masterIp}}
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        
        <h3>{{$t('dashboard.rsyncd_configuration')}}</h3>
        <div class="row">
          <div class="col-lg-12">
            <div class="col-md-6">
              <form class="form-horizontal">
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.rsyncd_status')}}
                  </label>
                  <div class="col-sm-5">
                    <span
                      :class="rsyncd.status == 'enabled' ? 'pficon pficon-ok' : 'pficon-off'"
                      data-toggle="tooltip"
                      data-placement="top"
                      :title="$t('dashboard.status')+': '+ (rsyncd.status == 'enabled' ? $t('dashboard.enabled') : $t('dashboard.disabled'))"
                    ></span>
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.rsyncd_port')}}
                  </label>
                  <div class="col-sm-5">
                    {{rsyncd.port}}
                  </div>
                </div>
                <div class="form-group">
                  <label class="col-sm-5 control-label">
                    {{$t('dashboard.rsyncd_password')}}
                  </label>
                  <div class="col-sm-5">
                    {{rsyncd.password}}
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  components: {
  },
  props: {
  },
  mounted() {
    this.getDashboardData()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      hotsync: {
        status: null,
        role: null,
        masterIp: null,
        slaveIp: null,
        slavePort: null,
        databases: null
      },
      rsyncd: {
        status: null,
        TCPPort: null,
        password: null
      }
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage
    },
    closeErrorMessage() {
      this.errorMessage = null
    },
    getDashboardData() {
      var context = this;
      context.uiLoaded = false;
      nethserver.exec(
        ["nethserver-hotsync/dashboard/read"],
        { action: "configuration" },
        null,
        function(success) {
          try {
            var json = JSON.parse(success);
            context.hotsync = json.hotsync;
            context.rsyncd = json.rsyncd;
            if (context.hotsync.role.trim() == "" || context.hotsync.role.trim() == "null") {
              context.hotsync.role = context.$i18n.t("dashboard.role_not_configured");
            }
            setTimeout(function() {
              $('[data-toggle="tooltip"]').tooltip();
            }, 250);
          } catch (e) {
            console.error(e);
          }
          context.uiLoaded = true;
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("dashboard.error_reading_hotsync_configuration"), error);
        }
      );
    }
  }
};
</script>

<style>
</style>