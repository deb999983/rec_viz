const func = "function log(x) {console.log(x);}";
const callable = eval(func);
console.log(callable);
callable("Hello world");
