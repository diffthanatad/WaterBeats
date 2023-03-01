module.exports = (sequelize, Sequelize) => {
    const User = sequelize.define("users", {
        name: {
            type: Sequelize.STRING(150),
            unique: false,
            allowNull: false
        },
        username: {
            type: Sequelize.STRING(150),
            unique: true,
            allowNull: false
        },
        password: {
            type: Sequelize.STRING(300),
            allowNull: false
        },
        disable: {
            type: Sequelize.BOOLEAN,
            defaultValue: false
        },
        role: {
            type: Sequelize.ENUM('admin', 'moderator', 'user'),
            defaultValue: 'user'
        }
    },
    {
        timestamps: false
    });

    return User;
};