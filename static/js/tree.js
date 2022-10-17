var TreeView = function () {

    return {
        //main function to initiate the module
        init: function () {

            var DataSourceTree = function (options) {
                this._data  = options.data;
                this._delay = options.delay;
            };

            DataSourceTree.prototype = {

                data: function (options, callback) {
                    var self = this;

                    setTimeout(function () {
                        var data = $.extend(true, [], self._data);

                        callback({ data: data });

                    }, this._delay)
                }
            };

            // INITIALIZING TREE
            var treeDataSource = new DataSourceTree({
                data: [
                    { name: '李自强', type: 'folder', additionalParameters: { id: 'F1' } },
                    { name: '李拓新', type: 'folder', additionalParameters: { id: 'F2' } },
                    { name: '李弘毅', type: 'item', additionalParameters: { id: 'I1' } },
                    { name: '李求是', type: 'item', additionalParameters: { id: 'I2' } }
                ],
                delay: 400
            });

            // var treeDataSource2 = new DataSourceTree({
            //     data: [
            //         { name: 'Test tree 1 <div class="tree-actions"></div>', type: 'folder', additionalParameters: { id: 'F11' } },
            //         { name: 'Test tree 2 <div class="tree-actions"></div>', type: 'folder', additionalParameters: { id: 'F12' } },
            //         { name: '<i class="fa fa-bell-o"></i> Notification', type: 'item', additionalParameters: { id: 'I11' } },
            //         { name: '<i class="fa fa-bar-chart-o"></i> Assignment', type: 'item', additionalParameters: { id: 'I12' } }
            //     ],
            //     delay: 400
            // });

            // var treeDataSource3 = new DataSourceTree({
            //     data: [
            //         { name: '李自强 <div class="tree-actions"></div>', type: 'folder', additionalParameters: { id: 'F11' } },
            //         { name: '李拓新 <div class="tree-actions"></div>', type: 'folder', additionalParameters: { id: 'F12' } },
            //         { name: '李弘毅', type: 'item', additionalParameters: { id: 'I11' } },
            //         { name: '李求是', type: 'item', additionalParameters: { id: 'I12' } }
            //     ],
            //     delay: 400
            // });

            // var treeDataSource4 = new DataSourceTree({
            //     data: [
            //         { name: '李自强<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F11' } },
            //         { name: '李拓新<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F12' } },
            //         { name: '<i class="fa fa-user"></i> User <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div><div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I11' } },
            //         { name: '<i class="fa fa-calendar"></i> Events <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } },
            //         { name: '<i class="fa  fa-gear "></i> Works <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } }
            //     ],
            //     delay: 400
            // });

            // var treeDataSource5 = new DataSourceTree({
            //     data: [
            //         { name: '李自强<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F11' } },
            //         { name: '李拓新<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F12' } },
            //         { name: '<i class="fa fa-user"></i> User <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div><div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I11' } },
            //         { name: '<i class="fa fa-calendar"></i> Events <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } },
            //         { name: '<i class="fa  fa-gear "></i> Works <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } }
            //     ],
            //     delay: 400
            // });

            // var treeDataSource6 = new DataSourceTree({
            //     data: [
            //         { name: '李自强<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F11' } },
            //         { name: '李拓新<div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'folder', additionalParameters: { id: 'F12' } },
            //         { name: '<i class="fa fa-user"></i> User <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div><div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I11' } },
            //         { name: '<i class="fa fa-calendar"></i> Events <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } },
            //         { name: '<i class="fa  fa-gear "></i> Works <div class="tree-actions"><i class="fa fa-plus"></i><i class="fa fa-trash-o"></i><i class="fa fa-refresh"></i></div>', type: 'item', additionalParameters: { id: 'I12' } }
            //     ],
            //     delay: 400
            // });

            $('#FlatTree').tree({
                dataSource: treeDataSource,
                loadingHTML: '<img src="/static/img/input-spinner.gif"/>',
            });


            // $('#FlatTree2').tree({
            //     dataSource: treeDataSource2,
            //     loadingHTML: '<img src="/static/img/input-spinner.gif"/>',
            // });

            // $('#FlatTree3').tree({
            //     dataSource: treeDataSource3,
            //     loadingHTML: '<img src="/static/img/input-spinner.gif"/>',
            // });

            // $('#FlatTree4').tree({
            //     selectable: false,
            //     dataSource: treeDataSource4,
            //     loadingHTML: '<img src="/static/img/input-spinner.gif"/>',
            // });


        }

    };

}();