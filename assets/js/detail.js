    var creole;
    $(document).ready(function() {
	// TODO initialise using ajax and on demand
	creole = new Parse.Simple.Creole( {
	    forIE: document.all,
	    interwiki: {
		WikiCreole: 'http://www.wikicreole.org/wiki/',
		Wikipedia: 'http://en.wikipedia.org/wiki/'
	    },
	    linkFormat: ''
	} );
	$('.tabbable').on('shown', '.link_edit', function(e) {
	    var par_id = GetParId(e.target);
	    $("#form_"+par_id).find("textarea,:text").each(function(i, e) {
		UpdatePreview(e)});
	});
	$('.tabbable').on('shown', '.link_compare', function(e) {
	    var par_id = GetParId(e.target);
	    Compare(par_id);
	});
	$('#main').bind('keyup paste change', function(e) {
	    UpdatePreview(e.srcElement);
	});
	$('.link_view').data("content", "View the paragraph in its current form.");
	$('.link_edit').data("content", "Make the paragraph better by editing it.");
	$('.link_compare').data("content", "See the changes you've just made, commit or undo them.");
	$('.btn_reset').data("content", "Undo your changes and restore original text.");
	$('.btn_commit').data("content", "Save your changes for the others to see.");
	$('.link_view,.link_edit,.link_compare,.btn_reset,.btn_commit').data("title", "What's that?");
	$('.link_view,.link_edit,.link_compare,.btn_reset,.btn_commit').popover();
    });

// Gets NOT a jquery object
function UpdatePreview(trigger) {
    var par_id = GetParId(trigger);
    if (trigger.name=="text") {
	var target = document.getElementById("preview_"+par_id);
	target.innerHTML="&nbsp";
	creole.parse(target, trigger.value);
	MathJax.Hub.Queue(["Typeset",MathJax.Hub,"preview_"+par_id]);
    } else if (trigger.name=="title") {
	$("#title_"+par_id).html("<h3>"+trigger.value+"&nbsp<h3>");
    }
}

function ResetEdit(par_id) {
    if (par_id=="add") {
	$("#form_"+par_id).find("textarea").val("");
    } else {
	$("#form_"+par_id).find("textarea").val(window["orig_pars"][par_id]);
    }
    // TODO(kazeevn) reset title as well
    //    $("#form_"+par_id).find("text[name=title]").val(orig_pars[par_id]);
    $("#tabbable_"+par_id).find(".tab-pane,li").removeClass("active");
    $("#tabbable_"+par_id).find(".link_edit").addClass("active in");
    $("#edit_"+par_id).addClass("active");
    $("#form_"+par_id).find("textarea,:text").each(function(i, e) {
	UpdatePreview(e)});
}

function GetParId(element) {
    return $(element).parents("[data-par-id]").data("par-id");
}

function  Preview(par_id)
{
    var options = {
	target: "#preview_"+par_id,
	url: "{% url notes.views.preview %}",
	success: function() {
            MathJax.Hub.Queue(["Typeset",MathJax.Hub,"preview_"+par_id]);
	}};
    $("#form_"+par_id).ajaxSubmit(options);

};
function ToogleImage(par_id)
{
    $("#image_"+par_id).attr("src", document.location+par_id+"/image");
};

function Compare(par_id)
{
    var base = difflib.stringAsLines(window["orig_pars"][par_id]);
    var newtxt = difflib.stringAsLines($("#form_"+par_id).find("textarea").val());
    var sm = new difflib.SequenceMatcher(base, newtxt);
    var opcodes = sm.get_opcodes();
    var diffoutputdiv = document.getElementById("compare_"+par_id);
    while (diffoutputdiv.firstChild) diffoutputdiv.removeChild(diffoutputdiv.firstChild);
    var contextSize = 3;
    contextSize = contextSize ? contextSize : null;
    diffoutputdiv.appendChild(diffview.buildView({ baseTextLines:base,
						   newTextLines:newtxt,
						   opcodes:opcodes,
						   baseTextName:"Was",
						   newTextName:"After your edit",
						   contextSize:contextSize,
						   viewType: 0}));


};
function Commit(par_id)
{
    var options = {
	target: "#view_"+par_id,
	success: function() {
	    MathJax.Hub.Queue(["Typeset",MathJax.Hub,"view_"+par_id]);
	}};
    $("#form_"+par_id).ajaxSubmit(options);

    if (par_id=="add") {
	setTimeout(function() {
            location.replace("/notes/{{ note.id }}/");}, 700);
    } else {
	  window["orig_pars"][par_id]= $("#form_"+par_id).find("textarea[name=text]").val();
	  }
    $("#tabbable_"+par_id).find(".tab-pane,li").removeClass("active");
    $("#view_"+par_id).addClass("active");
    $("#tabbable_"+par_id).find(".link_view").addClass("active in");
};
function AddPar() {
    $("#add").css('display', 'inline')
};
