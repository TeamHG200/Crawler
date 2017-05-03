<template>


<div class="row" style="margin-top:10px">

    <div class="col-lg-3">
      <div class="panel panel-default"  name="search-planner-group">
        <div class="panel-heading">
          <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 正向情感
            <button class="btn btn-success btn-circle pull-right" v-on:click="set_word('/file/ntusd/ntusd-positive.txt', positive)">
              <i class="fa fa-check fa-fw"></i>
            </button>
        </div>
        <div class="panel-body" style="min-height:190px" id="all_projects">
          <textarea rows="30" class="form-control" v-model="positive"></textarea>
        </div>
      </div>
    </div>

    <div class="col-lg-3">
      <div class="panel panel-default"  name="search-planner-group">
        <div class="panel-heading">
          <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 负向情感
            <button class="btn btn-success btn-circle pull-right" v-on:click="set_word('/file/ntusd/ntusd-negative.txt', negative)">
              <i class="fa fa-check fa-fw"></i>
            </button>
        </div>
        <div class="panel-body" style="min-height:190px" id="all_projects">
          <textarea rows="30" class="form-control" v-model="negative"></textarea>
        </div>
      </div>
    </div>

    <div class="col-lg-3">
      <div class="panel panel-default"  name="search-planner-group">
        <div class="panel-heading">
          <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 程度词
            <button class="btn btn-success btn-circle pull-right" v-on:click="set_word('/file/ntusd/ntusd-adj.txt', adj)">
              <i class="fa fa-check fa-fw"></i>
            </button>
        </div>
        <div class="panel-body" style="min-height:190px" id="all_projects">
          <textarea rows="30" class="form-control" v-model="adj"></textarea>
        </div>
      </div>
    </div>

    <div class="col-lg-3">
      <div class="panel panel-default"  name="search-planner-group">
        <div class="panel-heading">
          <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 转意词
            <button class="btn btn-success btn-circle pull-right" v-on:click="set_word('/file/ntusd/ntusd-adv.txt', adv)">
              <i class="fa fa-check fa-fw"></i>
            </button>
        </div>
        <div class="panel-body" style="min-height:190px" id="all_projects">
          <textarea rows="30" class="form-control" v-model="adv"></textarea>
        </div>
      </div>
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
            positive : "",
            negative : "",
            adj : "",
            adv : "",
        }
    },
    created:function(){
        this.show_positive()
        this.show_negative()
        this.show_adj()
        this.show_adv()
    },
    methods: {

        show_positive:function() {
            this.$http.get("/file/ntusd/ntusd-positive.txt",{
                params: {
                }})
                .then(function (resp) {
                    this.$data.positive = resp.data
                },function(){
                    alert("网络不通")
                })

        },

        show_negative:function() {
            this.$http.get("/file/ntusd/ntusd-negative.txt",{
                params: {
                }})
                .then(function (resp) {
                    this.$data.negative = resp.data
                },function(){
                    alert("网络不通")
                })
        },

        show_adj:function() {
            this.$http.get("/file/ntusd/ntusd-adj.txt",{
                params: {
                }})
                .then(function (resp) {
                    this.$data.adj = resp.data
                },function(){
                    alert("网络不通")
                })
        },

        show_adv:function() {
            this.$http.get("/file/ntusd/ntusd-adv.txt",{
                params: {
                }})
                .then(function (resp) {
                    this.$data.adv = resp.data
                },function(){
                    alert("网络不通")
                })
        },

        set_word:function(path, value) {
            this.$http.post(path,{
                content: value,
            })
                .then(function (resp) {
                },function(){
                })
        }
    }

}


</script>
