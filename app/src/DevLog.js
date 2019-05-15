/* eslint-disable */

/**
 * This class only logs into the console during development
 * (When NODE_ENV=development )
 */
export default class DevLog {
  static log(args) {
    if (process.env['NODE_ENV'] === 'development') {
      console.log(args);
    }
  }

  static error(args) {
    if (process.env['NODE_ENV'] === 'development') {
      console.error(args);
    }
  }

  static info(args) {
    if (process.env['NODE_ENV'] === 'development') {
      console.info(args);
    }
  }

  static warn(args) {
    if (process.env['NODE_ENV'] === 'development') {
      console.warn(args);
    }
  }

  static debug(args) {
    if (process.env['NODE_ENV'] === 'development') {
      console.debug(args);
    }
  }
}
