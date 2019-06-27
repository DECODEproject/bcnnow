/* global window, require, define, module */
/* eslint-env node, mocha */
(function() {

  var relativeTimeRe = /([-+])(\d*)\s*(minutes|minute|min|Min|Minute|Minutes|hr|Hr|hours|hour|Hour|Hours|days|day|Days|Day|weeks|week|Week|Weeks|months|month|mon|Month|Months|years|year|Year|Years|Quarters|Quarter|seconds|second|Seconds|Second|sec|s|m|h|d|D|M|y|Y|q|Q|Qr|qr|ms|w|wk|Wk)/,
    initialize,
    convertCase;

  convertCase = ({
    'ms': 'milliseconds',
    's': 'seconds',
    'sec': 'seconds',
    'second': 'seconds',
    'seconds': 'seconds',
    'Second': 'seconds',
    'Seconds': 'seconds',
    'm': 'minutes',
    'min': 'minutes',
    'minute': 'minutes',
    'minutes': 'minutes',
    'Min': 'minutes',
    'Minute': 'minutes',
    'Minutes': 'minutes',
    'h': 'hours',
    'hr': 'hours',
    'Hr': 'hours',
    'hour': 'hours',
    'hours': 'hours',
    'Hour': 'hours',
    'Hours': 'hours',
    'd': 'days',
    'D': 'days',
    'day': 'days',
    'days': 'days',
    'Day': 'days',
    'Days': 'days',
    'w': 'weeks',
    'W': 'weeks',
    'wk': 'weeks',
    'Wk': 'weeks',
    'week': 'weeks',
    'weeks': 'weeks',
    'Week': 'weeks',
    'Weeks': 'weeks',
    'M': 'months',
    'mon': 'months',
    'month': 'months',
    'months': 'months',
    'Month': 'months',
    'Months': 'months',
    'y': 'years',
    'Y': 'years',
    'yr': 'years',
    'yrs': 'years',
    'year': 'years',
    'years': 'years',
    'Year': 'years',
    'Years': 'years',
    'q': 'quarters',
    'qr': 'quarters',
    'Q': 'quarters',
    'Qr': 'quarters',
    'qtr': 'quarters',
    'quarter': 'quarters',
    'quarters': 'quarters',
    'Quarter': 'quarters',
    'Quarters': 'quarters'
  });

  initialize = function(moment) {

    moment.fn.advancedTime = function(relativeTimeString) {
      var result;
      relativeTimeString = relativeTimeString.trim();
      if (relativeTimeRe.test(relativeTimeString)) {
          result = relativeTimeRe.exec(relativeTimeString);
          if (relativeTimeString.charAt(0) === '-') {
            return moment(this).subtract(+result[2], convertCase[result[3]]);
          }
          return moment(this).add(+result[2], convertCase[result[3]]);
      } else {
        return moment(relativeTimeString);
      }
    };

    moment.fn.isRelativeTimeFormat = function(relativeTimeString) {
      relativeTimeString = relativeTimeString.trim();
      if (relativeTimeString === 'now') {
        return true;
      }
      return relativeTimeRe.test(relativeTimeString);
    };

    return moment;
  };

  if (typeof define === 'function' && define.amd) {
    define('moment-relative-time', ['moment'], function(moment) {
      return initialize(moment);
    });
  } else if (typeof module !== 'undefined') {
    module.exports = initialize(require('moment'));
  } else if (typeof window !== 'undefined' && window.moment) {
    this.moment = initialize(this.moment);
  }

}).call(this);
