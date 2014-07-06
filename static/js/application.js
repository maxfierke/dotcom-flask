jQuery(function ($) {
    'use strict';

    var mfcom = {
        selectors: {
            emailText: '.liame',
            filters: {
                all: '#all',
                categories: '.js-filter'
            },
            nav: {
                active: 'active',
                current: '.nav li:has(a[href="'+window.location.pathname+'"])'
            },
            projectPanel: '.panel-project',
            tooltips: '.js-tooltip'
        },
        states: {
            selected: 'btn-primary',
            unselected: 'btn-default'
        },
        registerEmailIlluminationEvents: function () {
            $(mfcom.selectors.emailText).hover(function () {
                this.href = '\x6D\x61\x69\x6C\x74\x6F\x3A' + this.text;
            });
        },

        registerProjectFilterEvents: function () {
            $(mfcom.selectors.filters.all).on('click', function() {
                $(mfcom.selectors.filters.categories).removeClass(mfcom.states.selected).addClass(mfcom.states.unselected);
                $(this).addClass(mfcom.states.selected);
                $(mfcom.selectors.projectPanel).show({ easing: "swing", duration: 400 });
                return false;
            });
            $(mfcom.selectors.filters.categories).on('click', function() {
                var filterClass = "."+$(this).attr('id');
                $(mfcom.selectors.filters.all).removeClass(mfcom.states.selected).addClass(mfcom.states.unselected);
                $(mfcom.selectors.filters.categories).removeClass(mfcom.states.selected).addClass(mfcom.states.unselected);
                $(mfcom.selectors.projectPanel).not(filterClass).hide({ easing: "swing", duration: 400 });
                $(filterClass).show({ easing: "swing", duration: 400 });
                $(this).removeClass(mfcom.states.unselected).addClass(mfcom.states.selected);
                return false;
            });
        },

        populateLatestProject: function () {
            var $lp = $('#latest-project');

            if ($lp.length > 0) {
                $.get('/api/project', function(data) {
                    var proj = data.data[0];
                    $lp.find('.project-title a').text(proj.name).prop('href', '/projects/#'+proj.project_id);
                    if (proj.image) {
                        $lp.find('.project-img').prop('src', '/api/project/'+proj.project_id+'/thumbnail').removeClass('hidden');
                    }
                    $lp.find('.project-shortdesc').text(proj.short_description);
                    var $pt = $lp.find('.project-tags');
                    for (var i in proj.categories) {
                        $pt.append('<li><span class="label label-primary"><a href="/projects#'+proj.categories[i].slug+'">'+proj.categories[i].name+'</a></span></li>');
                    }
                });
            }
        },

        init: function () {
            // Highlight current nav item
            $(mfcom.selectors.nav.current).addClass('active');

            // Activate bootstrap tooltips.
            $(mfcom.selectors.tooltips).tooltip();

            mfcom.registerEmailIlluminationEvents();
            mfcom.registerProjectFilterEvents();
            mfcom.populateLatestProject();
        }
    };

    mfcom.init();
});
