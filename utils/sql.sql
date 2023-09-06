CREATE TABLE IF NOT EXISTS expert_ai_rlhf (
	id BIGSERIAL PRIMARY KEY,
	did INT NOT NULL,
	category varchar NOT NULL,
	paragraph1 INT NOT NULL,
	paragraph2 INT NOT NULL,
	metadata jsonb NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL
	topic varchar NULL
);

ALTER TABLE expert_ai_rlhf ADD COLUMN topic varchar NULL;

update expert_ai_rlhf
set topic = 'iran-russia-hormuz'
where topic is null;

