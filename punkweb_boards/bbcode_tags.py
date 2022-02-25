from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class SpoilerTag(BBCodeTag):
    name = "spoiler"
    definition_string = "[spoiler={TEXT1}]{TEXT2}[/spoiler]"
    format_string = """
    <div class="spoiler">
        <button class="pw-button-raised spoiler__open" type="button">
            Spoiler: {TEXT1}
        </button>
        <div class="spoiler__content">
            {TEXT2}
        </div>
    </div>"""


class SizeTag(BBCodeTag):
    name = "size"
    definition_string = "[size={RANGE=1,7}]{TEXT}[/size]"
    format_string = '<font size="{RANGE=1,7}">{TEXT}</font>'


class UserTag(BBCodeTag):
    name = "user"
    definition_string = "[user]{TEXT}[/user]"
    format_string = """<a href="/board/profile/{TEXT}/"><i class="fa fa-user" aria-hidden="true"></i> {TEXT}</a>"""


class CodeTag(BBCodeTag):
    name = "code"
    definition_string = "[code]{TEXT}[/code]"
    format_string = '<pre class="prettyprint"><code>{TEXT}</code></pre>'

    class Options:
        render_embedded = False


class SubscriptTag(BBCodeTag):
    name = "sub"
    definition_string = "[sub]{TEXT}[/sub]"
    format_string = "<sub>{TEXT}</sub>"


class SuperscriptTag(BBCodeTag):
    name = "sup"
    definition_string = "[sup]{TEXT}[/sup]"
    format_string = "<sup>{TEXT}</sup>"


class FontTag(BBCodeTag):
    name = "font"
    definition_string = "[font={TEXT1}]{TEXT2}[/font]"
    format_string = '<span style="font-family:{TEXT1}">{TEXT2}</span>'


class UlTag(BBCodeTag):
    name = "ul"
    definition_string = "[ul]{TEXT}[/ul]"
    format_string = "<ul>{TEXT}</ul>"


class OlTag(BBCodeTag):
    name = "ol"
    definition_string = "[ol]{TEXT}[/ol]"
    format_string = "<ol>{TEXT}</ol>"


class LiTag(BBCodeTag):
    name = "li"
    definition_string = "[li]{TEXT}[/li]"
    format_string = "<li>{TEXT}</li>"


class TableTag(BBCodeTag):
    name = "table"
    definition_string = "[table]{TEXT}[/table]"
    format_string = """<table class="table full-width">{TEXT}</table>"""


class TableTRTag(BBCodeTag):
    name = "tr"
    definition_string = "[tr]{TEXT}[/tr]"
    format_string = "<tr>{TEXT}</tr>"


class TableTHTag(BBCodeTag):
    name = "th"
    definition_string = "[th]{TEXT}[/th]"
    format_string = "<th>{TEXT}</th>"


class TableTDTag(BBCodeTag):
    name = "td"
    definition_string = "[td]{TEXT}[/td]"
    format_string = "<td>{TEXT}</td>"


class HrTag(BBCodeTag):
    name = "hr"
    definition_string = "[hr]"
    format_string = "<hr/>"

    class Options:
        standalone = True


class ShadowTag(BBCodeTag):
    name = "shadow"
    definition_string = "[shadow={TEXT1}]{TEXT2}[/shadow]"
    format_string = """<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em {TEXT1}">{TEXT2}</span>"""


class AnchorTag(BBCodeTag):
    name = "anchor"
    definition_string = "[anchor]{TEXT}[/anchor]"
    format_string = """<div class="anchorPoint"><a name="{TEXT}"></a><i class="fa fa-anchor fa-fw"></i><span style="font-style: italic">#{TEXT}</span></div>"""


class QuoteTag(BBCodeTag):
    name = "quote"
    definition_string = "[quote={TEXT1}]{TEXT2}[/quote]"
    format_string = """
        <blockquote>
            <cite>
                <a href="/board/profile/{TEXT1}/">
                <i class="fa fa-user" aria-hidden="true"></i> {TEXT1}</a> said:
            </cite>
            {TEXT2}
        </blockquote>"""


class UncheckedBoxTag(BBCodeTag):
    name = "n"
    definition_string = "[n]{TEXT}"
    format_string = """
        <label for="bbunchecked"><input name="bbunchecked" type="checkbox" disabled="disabled" /> {TEXT}</label>"""

    class Options:
        newline_closes = True
        same_tag_closes = True
        end_tag_closes = True
        strip = True


class CheckedBoxTag(BBCodeTag):
    name = "y"
    definition_string = "[y]{TEXT}"
    format_string = """<label for="bbchecked"><input name="bbchecked" type="checkbox" disabled="disabled" checked="checked" /> {TEXT}</label>"""

    class Options:
        newline_closes = True
        same_tag_closes = True
        end_tag_closes = True
        strip = True


class EscapeTag(BBCodeTag):
    name = "escape"
    definition_string = "[escape]{TEXT}[/escape]"
    format_string = """<div class="escaped">{TEXT}</div>"""

    class Options:
        render_embedded = False


class YoutubeTag(BBCodeTag):
    name = "youtube"
    definition_string = "[youtube]{TEXT}[/youtube]"
    format_string = """<iframe width="560" height="315" frameborder="0" src="https://www.youtube-nocookie.com/embed/{TEXT}?wmode=opaque" data-youtube-id="{TEXT}" allowfullscreen></iframe>"""


class EmailTag(BBCodeTag):
    name = "email"
    definition_string = "[email={TEXT1}]{TEXT2}[/email]"
    format_string = """<a href="mailto:{TEXT1}">{TEXT2}</a>"""


class EmailTag(BBCodeTag):
    name = "email"
    definition_string = "[email={TEXT1}]{TEXT2}[/email]"
    format_string = """<a href="mailto:{TEXT1}">{TEXT2}</a>"""


class LeftTag(BBCodeTag):
    name = "left"
    definition_string = "[left]{TEXT}[/left]"
    format_string = """<div style="text-align: left">{TEXT}</div>"""


class RightTag(BBCodeTag):
    name = "right"
    definition_string = "[right]{TEXT}[/right]"
    format_string = """<div style="text-align: right">{TEXT}</div>"""


class JustifyTag(BBCodeTag):
    name = "justify"
    definition_string = "[justify]{TEXT}[/justify]"
    format_string = """<div style="text-align: justify">{TEXT}</div>"""


class RTLTag(BBCodeTag):
    name = "rtl"
    definition_string = "[rtl]{TEXT}[/rtl]"
    format_string = """<div style="direction: rtl">{TEXT}</div>"""


class LTRTag(BBCodeTag):
    name = "ltr"
    definition_string = "[ltr]{TEXT}[/ltr]"
    format_string = """<div style="direction: ltr">{TEXT}</div>"""


tag_pool.register_tag(SpoilerTag)
tag_pool.register_tag(SizeTag)
tag_pool.register_tag(UserTag)
tag_pool.register_tag(CodeTag)
tag_pool.register_tag(SubscriptTag)
tag_pool.register_tag(SuperscriptTag)
tag_pool.register_tag(FontTag)
tag_pool.register_tag(UlTag)
tag_pool.register_tag(OlTag)
tag_pool.register_tag(LiTag)
tag_pool.register_tag(TableTag)
tag_pool.register_tag(TableTRTag)
tag_pool.register_tag(TableTHTag)
tag_pool.register_tag(TableTDTag)
tag_pool.register_tag(HrTag)
tag_pool.register_tag(ShadowTag)
tag_pool.register_tag(AnchorTag)
tag_pool.register_tag(QuoteTag)
tag_pool.register_tag(UncheckedBoxTag)
tag_pool.register_tag(CheckedBoxTag)
tag_pool.register_tag(EscapeTag)
tag_pool.register_tag(YoutubeTag)
tag_pool.register_tag(EmailTag)
tag_pool.register_tag(LeftTag)
tag_pool.register_tag(RightTag)
tag_pool.register_tag(JustifyTag)
tag_pool.register_tag(RTLTag)
tag_pool.register_tag(LTRTag)
