<template>

<div class="panel panel-default"  name="search-planner-group">


<!-- create -->
    <div class="modal fade" id="myModalNewGameReview" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="myModalLabel">
                        新建抓取
                    </h4>
                </div>
                <div class="modal-body">
                  <div class="form-group">
                    <input class="form-control" placeholder="game id" v-model="game_id"></input>
                  </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal" v-on:click="crawler()">抓取</button>
                </div>
            </div><!-- /.modal-content -->
        </div><!-- /.modal -->
    </div>


  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 评论 {{status}}
    <button class="btn btn-success btn-circle pull-right" data-toggle="modal" data-target="#myModalNewGameReview" >
       <i class="fa fa-plus fa-fw"></i>
    </button>
  </div>

  <!-- /.panel-heading -->

  <div class="panel-body">
    <table width="100%" class="table table-striped table-bordered table-hover" id="dataTables-example">
      <thead>
        <tr>
         <th>ID</th>
         <th>Game</th>
         <th>Reviews</th>
         <th>Useful</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd gradeX" v-for="review in reviews">
          <td>{{ review.review_id }}</td>
          <td>{{ review.game_id }}</td>
          <td>{{ review.text }}</td>
          <td>
             <button v-if="review.score==0||review.score==1" class="btn btn-outline btn-primary btn-circle pull-right" style="margin-top:0px;margin-left:2px" data-toggle="popover" data-placement="top" data-content="差评" v-on:click="zan(2,review.review_id)">
               <i class="fa  fa-thumbs-o-down fa-fw"></i>
             </button>
             <button v-if="review.score==2" class="btn btn-danger btn-circle pull-right" style="margin-top:0px;margin-left:2px" data-toggle="popover" data-placement="top" data-content="差评" v-on:click="zan(0,review.review_id)">
               <i class="fa  fa-thumbs-o-down fa-fw"></i>
             </button>
             <button v-if="review.score==0||review.score==2" class="btn btn-outline btn-primary btn-circle pull-right" data-toggle="popover" data-placement="top" data-content="好评" v-on:click="zan(1,review.review_id)">
               <i class="fa  fa-thumbs-o-up fa-fw"></i>
             </button>
             <button v-if="review.score==1" class="btn btn-success btn-circle pull-right" data-toggle="popover" data-placement="top" data-content="好评" v-on:click="zan(0,review.review_id)">
               <i class="fa  fa-thumbs-o-up fa-fw"></i>
             </button>
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
            reviews: [],
            game_id : "",
            status : "",
            review_count : 0,
            pages: [],
        }
    },
    created:function(){
        this.reload_view()
    },
    methods: {

        reload_view:function() {
            this.$data.status = "正在载入..."
            this.$http.get("/review_count",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.review_count = data.count
                        this.show_review()
                    }
                },function(){
                    alert("网络不通")
                })
        },

        show_review:function() {
            this.$http.get("/reviews",{
                params: {
                    s: "0",
                    n: this.$data.review_count
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.status = ""
                        this.$data.reviews = data
                        setTimeout(() => {
                            $('#dataTables-example').DataTable({
                                destroy: true
                            });
                        }, 100)
                    }
                },function(){
                    alert("网络不通")
                })

        },

        crawler:function() {
            this.$data.status = "正在抓取中..."
            this.$http.get("/crawler",{
                params: {
                    gid: this.$data.game_id
                }})
                .then(function (resp) {
                    this.reload_view()
                },function(){
                    alert("网络不通")
                })
        },

        zan:function(s, review_id) {
            this.$http.get("/do_score",{
                params: {
                    review_id: review_id,
                    score: s
                }})
                .then(function (resp) {
                    this.$data.reviews[review_id-1].score = s
                },function(){
                    alert("网络不通")
                })
        }

    }

}


</script>
