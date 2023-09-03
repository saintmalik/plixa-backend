# import graphql_jwt
import graphene

# from graphene import ObjectType, Decimal, Field, List, Schema, String, Int, Mutation, Date, Boolean

# from django.db.models import Q
# from graphql import GraphQLError
# from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations




# ==========================================================================================
# ========================= PLIXA MUTATION SCHEMA TO CREATE NEW USER =======================
# ==========================================================================================



class AuthMutation(graphene.ObjectType):

    # REGISTER FIELDS
    register = mutations.Register.Field()

    # VERIFY ACCOUNT FIELDS
    verify_account = mutations.VerifyAccount.Field() 

    # UPDATE ACCOUNT FIELDS
    update_account = mutations.UpdateAccount.Field()

    # DELETE ACCOUNT FIELDS
    delete_account = mutations.DeleteAccount.Field()
    
    # RESEND ACTIVATION EMAIL
    resend_activation_email = mutations.ResendActivationEmail.Field()

    # SWAP EMAIL FIELDS 
    swap_emails = mutations.SwapEmails.Field()

    # PASSWORD RESET FIELDS
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()


    # TOKEN FIELDS
    token_auth = mutations.ObtainJSONWebToken.Field()

    # REFRESH TOKEN FIELDS
    refresh_token = mutations.RefreshToken.Field()

    # VERIFY TOKEN
    verify_token = mutations.VerifyToken.Field()

    # REVOKE TOKEN
    revoke_token = mutations.RevokeToken.Field()

