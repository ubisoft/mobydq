/*Connect to database*/
\connect mobydq



/*Create table notification*/
/*Consider adding indexes on foreign keys in the future to improve performances*/
CREATE TABLE base.notification (
    id SERIAL PRIMARY KEY
  , message TEXT
  , status TEXT
  , flag_read BOOLEAN DEFAULT FALSE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , batch_id INTEGER REFERENCES base.batch(id)
  , data_source_id INTEGER REFERENCES base.data_source(id)
);

COMMENT ON TABLE base.notification IS
E'@omit update,delete\nNotifications pushed during the execution of batches tests of data sources.';



/*Create function to create notification message*/
CREATE OR REPLACE FUNCTION base.create_notification_message()
RETURNS TRIGGER AS $$
DECLARE
    object_type TEXT; -- Expected values: batch, data_source
    notification_message TEXT;
BEGIN
    object_type = TG_ARGV[0];
    
    -- Build and insert notification message for batch
    IF object_type = 'batch' THEN
      notification_message = 'Status of batch Id ' || NEW.id || ' set to ' || NEW.status;
      INSERT INTO base.notification (message, batch_id, status) VALUES (notification_message, NEW.id, NEW.status);
    
    -- Build and insert notification message for data source
    ELSEIF object_type = 'data_source' THEN
      notification_message = 'Status of data source ' || NEW.name || ' set to ' || NEW.connectivity_status;
      INSERT INTO base.notification (message, data_source_id, status) VALUES (notification_message, NEW.id, NEW.connectivity_status);
    END IF;

    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.create_notification_message IS
'Function used to send notification to frontend via GraphQL subscriptions.';



/*Create function to send notification to frontend using GraphQL subscriptions*/
CREATE OR REPLACE FUNCTION base.send_notification()
RETURNS TRIGGER AS $$
BEGIN
    -- First argument of PG_NOTIFY is the channel, it must contain 'postgraphile:' to be captured by PostGraphile simple subscriptions
    PERFORM(SELECT PG_NOTIFY('postgraphile:notification', JSON_BUILD_OBJECT('__node__', JSON_BUILD_ARRAY('Notification', NEW.id))::text));
    RETURN NEW;
END;
$$ language plpgsql;

COMMENT ON FUNCTION base.send_notification IS
'Function used to send notification to frontend via GraphQL subscriptions.';



/*Create function to mark all unread notifications as read*/
CREATE OR REPLACE FUNCTION base.mark_all_notifications_as_read()
RETURNS SETOF base.notification AS $$
BEGIN
    RETURN QUERY
    UPDATE base.notification
    SET flag_read=TRUE 
    WHERE flag_read=FALSE
    RETURNING *;
END;
$$ language plpgsql VOLATILE STRICT SECURITY DEFINER;

COMMENT ON FUNCTION base.mark_all_notifications_as_read IS
'Function used to mark all notifications of a user as read.';

REVOKE ALL ON FUNCTION base.mark_all_notifications_as_read FROM PUBLIC;



/*Triggers on insert*/
CREATE TRIGGER batch_insert_notification AFTER INSERT
ON base.batch FOR EACH ROW EXECUTE PROCEDURE base.create_notification_message('batch');

CREATE TRIGGER notification_insert_send AFTER INSERT
ON base.notification FOR EACH ROW EXECUTE PROCEDURE base.send_notification();



/*Triggers on update*/
CREATE TRIGGER batch_update_notification AFTER UPDATE
ON base.batch FOR EACH ROW WHEN (OLD.status <> NEW.status)
EXECUTE PROCEDURE base.create_notification_message('batch');

CREATE TRIGGER data_source_update_notification AFTER UPDATE
ON base.data_source FOR EACH ROW WHEN (OLD.connectivity_status <> NEW.connectivity_status)
EXECUTE PROCEDURE base.create_notification_message('data_source');