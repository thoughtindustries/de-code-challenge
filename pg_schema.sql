create table if not exists public.companies
(
    id uuid primary key,
    name varchar(65535),
    "updatedAt" timestamp without time zone
);

create table if not exists public.clients
(
    id uuid primary key,
    name varchar(65535),
    company uuid,
    "updatedAt" timestamp without time zone
);

create table if not exists public.users
(
    id uuid primary key,
    name varchar(65535),
    company uuid,
    client uuid,
    "updatedAt" timestamp without time zone
);

create table if not exists public."users_purchasedCourses"
(
    id uuid primary key,
    "user" uuid,
    course uuid,
    company uuid,
    status varchar(65535),
    "updatedAt" timestamp without time zone
);

alter table clients drop constraint if exists "clients_company_fkey";
alter table clients add constraint "clients_company_fkey" foreign key (company) references public.companies(id);
alter table users drop constraint if exists "users_company_fkey";
alter table users add constraint "users_company_fkey" foreign key (company) references public.companies(id);
alter table users drop constraint if exists "users_client_fkey";
alter table users add constraint "users_client_fkey" foreign key (client) references public.clients(id);
alter table "users_purchasedCourses" drop constraint if exists "users_company_fkey";
alter table "users_purchasedCourses" add constraint "users_company_fkey" foreign key (company) references public.companies(id);
