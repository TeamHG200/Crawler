<template>

<div class="panel panel-default"  name="search-planner-group">
  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 分词
    <input id="param" value="-t 2 -c 100" />
    <button class="btn btn-success btn-circle pull-right" v-on:click="show()">
       <i class="fa fa-check fa-fw"></i>
    </button>
  </div>

  <div class="panel-body">
    <canvas id="features" height="600" width="1130"></canvas>
  </div>

  <div class="panel-footer">
    <button id="color" onclick="nextColor()" >Change</button>
    <button id="run" onclick="drawModel()" >Run</button>
    <button id="clear" onclick="clearScreenAndData()" >Clear</button>
  </div>

</div>

</template>

<script>

export default{
    props: {
        user: String
    },
    data: function() {
        return {
            words: [],
            game_id : "",
            status : "",
            review_count : 0,
            pages: [],
        }
    },
    created:function(){

    },
    methods: {
        show:function() {
            init();
            addPoint(100,200);
            addPoint(200,100);
            addPoint(300,300);
            addPoint(100,200);
        },

        show_words:function() {
            this.$http.get("/words",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.status = ""
                        this.$data.words = data
                        setTimeout(() => {
                            $('#dataTables-example2').DataTable({
                                destroy: true
                            });
                        }, 100)
                    }
                },function(){
                    alert("网络不通")
                })

        },

        spliter:function() {
            this.$data.status = "正在分词提取..."
            this.$http.get("/split",{
                params: {
                }})
                .then(function (resp) {
                    this.show_words()
                },function(){
                    alert("网络不通")
                })
        }

    }

}


</script>
