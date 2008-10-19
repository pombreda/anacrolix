#include "miniplay.h"

static NotifyNotification *notify_ = NULL;

void mp_notify_init()
{
	notify_ = notify_notification_new_with_status_icon(
		"Summary", NULL, "miniplay/play-icon.svg", mp_get_status_icon());
}

static void
gstr_append(gchar **dest, gchar *src)
{
	gchar *temp;
	if (*dest) {
		temp = g_strconcat(*dest, src, NULL);
		g_free(*dest);
	} else {
		temp = g_strdup(src);
	}
	*dest = temp;
}

static void
gstr_appendfmt(gchar **dest, gchar const *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	gchar *temp = g_strdup_vprintf(fmt, ap);
	va_end(ap);
	gstr_append(dest, temp);
	g_free(temp);
}

void mp_notify_track(GstTagList const *tags)
{
	gchar *title = NULL, *artist = NULL, *album = NULL;
	gst_tag_list_get_string(tags, GST_TAG_TITLE, &title);
	gst_tag_list_get_string(tags, GST_TAG_ARTIST, &artist);
	gst_tag_list_get_string(tags, GST_TAG_ALBUM, &album);

	gchar *summary;
	if (title) {
		summary = title;
		title = NULL;
	} else {
		summary = g_strdup("");
	}

	gchar *body = NULL;
	if (artist) {
		gstr_appendfmt(&body, "by %s", artist);
		g_free(artist);
	}
	if (album) {
		gstr_appendfmt(&body, "%sfrom %s", artist?"\n":"", album);
		g_free(album);
	}
	if (!body)
		body = g_strdup("");

	notify_notification_update(notify_, summary, body, NULL);
	notify_notification_show(notify_, NULL);

	g_free(body);
	g_free(summary);
}
