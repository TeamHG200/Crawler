<template>

<div class="panel panel-default"  name="search-planner-group">
  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> SVM参数
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
            feature: [],
        }
    },
    created:function(){
        this.show_feature()
    },
    methods: {
        show:function() {
            init();
            for(var f in this.$data.feature){
                var score = this.$data.feature[f]
                var score2 = 600-score.score["2"]*10
                var score1 = score.score["1"]*15
                var useful = score.useful
                addPoint(score1, score2, useful);
            }
        },

        show_feature:function() {
            this.$http.get("/get_feature",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.status = ""
                        this.$data.feature = data
                    }
                },function(){
                    alert("网络不通")
                })

        }

    }

}


</script>
