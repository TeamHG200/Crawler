<template>

<div class="panel panel-default"  name="search-planner-group">


  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 向量化
    <button class="btn btn-success btn-circle pull-right" v-on:click="score()">
       <i class="fa fa-check fa-fw"></i>
    </button>
  </div>

  <!-- /.panel-heading -->

  <div v-if="status !=''" class="panel-body" style="min-height:190px" id="all_projects">
    <div class="fill">
        <h2 class="text-center">{{ status }}</h2>
    </div>
  </div>
  <div v-if="status == ''" class="panel-body" id="all_projects">
    <table width="100%" class="table table-striped table-bordered table-hover" id="dataTables-example3">
      <thead>
        <tr>
         <th>ID</th>
         <th>Game</th>
         <th>Score</th>
         <th>Useful</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd gradeX" v-for="f in feature">
          <td>{{ f.review_id }}</td>
          <td>{{ f.game_id }}</td>
          <td>
               <tbody>
                 <tr>
                     <td> 主观情感分 </td>
                     <td> {{f.score["1"]}} </td>
                 </tr>
                 <tr>
                     <td> 客观情感分 </td>
                     <td> {{f.score["2"]}} </td>
                 </tr>
               </tbody>
          </td>
          <td v-if="f.useful == 1">
              <a>好评</a>
          </td>
          <td v-if="f.useful == 2">
              <a>差评</a>
          </td>
        </tr>
      </tbody>
    </table>
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
            game_id : "",
            status : "",
            review_count : 0,
            pages: [],
        }
    },
    created:function(){
        this.show_feature()
    },
    methods: {

        show_feature:function() {
            this.$http.get("/get_feature",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.status = ""
                        this.$data.feature = data
                        setTimeout(() => {
                            $('#dataTables-example3').DataTable({
                                destroy: true
                            });
                        }, 100)
                    }
                },function(){
                    alert("网络不通")
                })

        },

        score:function() {
            this.$data.status = "正在向量分析..."
            this.$http.get("/do_feature",{
                params: {
                }})
                .then(function (resp) {
                    this.show_feature()
                },function(){
                    alert("网络不通")
                })
        }

    }

}


</script>
