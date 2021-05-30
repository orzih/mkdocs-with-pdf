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
  extends: ['standard', 'plugin:@typescript-eslint/recommended'],
  plugins: ['import', '@typescript-eslint'],
  // add your custom rules here
  rules: {
    'unicorn/number-literal-case': 'off'
  }
}
