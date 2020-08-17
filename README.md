python+requests+ddt+unittest自动化测试框架，用excel或mysql维护测试用例，支持接口依赖和数据清理  
1、分为excel和mysql两种维护用例的模式  
2、包含excel的多线程执行功能  
3、依赖case填写时只需填写其ID，依赖参数填写格式为${ },括号中为依赖返回中需要的字段  
4、depending_teardown字段填写的是依赖字段的清理接口id，且数量和位置需要和依赖case对应上，如果某位置无需清理，在该位置填写n即可  
5、mysql模式使用flask、flask-admin开发，支持用例单条执行和选中执行的功能  
6、参数和结果判断中可以填写关键字如int( )可把括号内的参数转为int，类似的还有bool( ),timestamp(n)生成n位的时间戳  
