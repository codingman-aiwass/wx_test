console.log("Script loaded successfully ");
Java.perform(function x() {
    console.log("Inside java perform function");
    //定位类
    var my_class = Java.use("com.roysue.demo02.MainActivity");
    console.log("Java.Use.Successfully!");//定位类成功！
    //在这里更改类的方法的实现（implementation）
    my_class.fun.implementation = function(x,y){
        //打印替换前的参数
        console.log( "original call: fun("+ x + ", " + y + ")");
        //把参数替换成2和5，依旧调用原函数
        var ret_value = this.fun(2, 5);
        return ret_value;
    }
});