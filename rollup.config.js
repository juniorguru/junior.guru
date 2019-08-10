import resolve from 'rollup-plugin-node-resolve';

module.exports = {
  input: 'juniorguru/js/main.js',
  output: {
    file: 'build/bundle.js',
    format: 'iife'
  },
  plugins: [resolve()]
};
