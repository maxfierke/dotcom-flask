'use strict';

var mfcom = {
    registerEmailIlluminationEvents: function () {
        $('.liame').hover(function () {
            this.href = '\x6D\x61\x69\x6C\x74\x6F\x3A' + this.text;
        });
    },

    registerProjectFilterEvents: function () {
        $("#all").on('click', function() {
            $("#all").addClass("btn-primary");
            $(".js-filter").removeClass("btn-primary").addClass("btn-default");
            $(".panel-project").show({ easing: "swing", duration: 400 });
            return false;
        });
        $(".js-filter").on('click', function() {
            var filterClass = $(this).attr('id');
            $("#js-project-filter a").removeClass("btn-primary").addClass("btn-default");
            $(".panel-project").not("."+filterClass).hide({ easing: "swing", duration: 400 });
            $("." + filterClass).show({ easing: "swing", duration: 400 });
            $(this).removeClass("btn-default").addClass("btn-primary");
            return false;
        });
    },

    populateLatestProject: function () {
        var $lp = $('#latest-project');

        if ($lp.length > 0) {
            $.get('/api/project', function(data) {
                var proj = data.projects[0];
                $lp.find('.project-title a').text(proj.name).prop('href', '/projects/#'+proj.project_id);
                if (proj.img.src) {
                    $lp.find('.project-img').prop('src', proj.img.src).removeClass('hide');
                }
                $lp.find('.project-shortdesc').text(proj.short_desc);
                var $pt = $lp.find('.project-tags');
                for (var i in proj.categories) {
                    $pt.append('<li><span class="label label-primary"><a href="/projects#'+proj.categories[i]+'">'+proj.categories[i]+'</a></span></li>');
                }
            });
        }
    },

    init: function () {
        // Highlight current nav item
        $('.nav a[href="'+window.location.pathname+'"]').parents('li').addClass('active');

        // Activate bootstrap tooltips.
        $('.js-tooltip').tooltip();

        this.registerEmailIlluminationEvents();
        this.registerProjectFilterEvents();
        this.populateLatestProject();
    }
};

mfcom.init();
