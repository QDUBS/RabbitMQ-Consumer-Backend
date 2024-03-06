from odoo.odoo import api


Contact = api.env["res.partner"]


def get_or_create_user(name, email, phone):
    try:
        user = Contact.search_read([("email", "=", email)], [
                                   "id", "email", "name", "phone"])[0]
        return user
    except IndexError:
        user = Contact.create({
            "email": email,
            "phone": phone,
            "name": name
        })
        return user
    except:
        return None
