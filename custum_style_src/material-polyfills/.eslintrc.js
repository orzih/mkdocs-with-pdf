module.exports = {
  root: true,
  env: {
    serviceworker: true,
    browser: true,
    node: true
  },
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2015
  },
  extends: ['prettier', 'plugin:prettier/recommended'],
  plugins: ['prettier'],
  // add your custom rules here
  rules: {
    'unicorn/number-literal-case': 'off'
  }
}
