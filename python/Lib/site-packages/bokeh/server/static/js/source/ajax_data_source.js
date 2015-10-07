(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(["underscore", "backbone", "common/logging", "./remote_data_source"], function(_, Backbone, Logging, RemoteDataSource) {
    var AjaxDataSource, AjaxDataSources, logger, _ref, _ref1;
    logger = Logging.logger;
    AjaxDataSource = (function(_super) {
      __extends(AjaxDataSource, _super);

      function AjaxDataSource() {
        this.update = __bind(this.update, this);
        this.setup = __bind(this.setup, this);
        this.destroy = __bind(this.destroy, this);
        _ref = AjaxDataSource.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      AjaxDataSource.prototype.type = 'AjaxDataSource';

      AjaxDataSource.prototype.destroy = function() {
        if (this.interval != null) {
          return clearInterval(this.interval);
        }
      };

      AjaxDataSource.prototype.setup = function(plot_view, glyph) {
        this.pv = plot_view;
        this.update();
        if (this.get('polling_interval')) {
          return this.interval = setInterval(this.update, this.get('polling_interval'));
        }
      };

      AjaxDataSource.prototype.update = function() {
        var _this = this;
        $.ajax({
          dataType: 'json',
          url: this.get('data_url'),
          xhrField: {
            withCredentials: true
          },
          method: this.get('method'),
          contentType: 'application/json'
        }).done(function(data) {
          _this.set('data', data);
          console.log(data);
          return null;
        }).error(function() {
          return console.log(arguments);
        });
        return null;
      };

      return AjaxDataSource;

    })(RemoteDataSource.RemoteDataSource);
    AjaxDataSources = (function(_super) {
      __extends(AjaxDataSources, _super);

      function AjaxDataSources() {
        _ref1 = AjaxDataSources.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      AjaxDataSources.prototype.model = AjaxDataSource;

      AjaxDataSources.prototype.defaults = {
        url: "",
        expr: null
      };

      return AjaxDataSources;

    })(Backbone.Collection);
    return {
      "Model": AjaxDataSource,
      "Collection": new AjaxDataSources()
    };
  });

}).call(this);

/*
//@ sourceMappingURL=ajax_data_source.js.map
*/